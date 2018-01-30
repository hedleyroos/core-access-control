import typing

from flask import jsonify

from . import mappings
from . import models
from . import settings
from .models import DB as db

ApiModel = typing.TypeVar("ApiModel")
SqlAlchemyModel = typing.TypeVar("SqlAlchemyModel")


def crud(
        model: typing.Type[SqlAlchemyModel],
        api_model: typing.Type[ApiModel],
        action: str,
        data: dict = None,
        query: dict = None) -> typing.Union[ApiModel, typing.List[ApiModel], None]:
    model = getattr(models, model)
    """
    Primary purpose of this method is to cut down on code duplication within
    the controller methods.

    It attempts to find a method based on the action that got passed along.
    In the event the method does not exist, it is left to raise an error, as
    this method can not be allowed to be implemented incorrectly.

    The SQLAlchemy model and API model classes are always passed to the action
    methods. While data and query data are passed along as kwargs for all
    methods. It is up to the specific method to make use of either or both as
    needed.
    Once again methods are left to raise errors, in this case KeyErrors if the
    required key and value is not present in data or query.

    :param model: SQLAlchemy model class.
    :param api_model: Swagger API model class
    :return: Swagger API model instance
    :return: List[Swagger API model instance]
    :return: None, only delete can return this.
    """
    return transform(
        globals()["%s_entry" % action](
            model=model,
            **{"data": data, "query": query}
        ),
        api_model=api_model
    )


def create_entry(model: typing.Type[SqlAlchemyModel], **kwargs) -> SqlAlchemyModel:
    """
    Instantiate a SQLAlchemy model instance and saves it to the corresponding
    database table.
    """
    instance = model(**kwargs["data"])
    db.session.add(instance)
    db.session.commit()
    return instance


def read_entry(model: typing.Type[SqlAlchemyModel], **kwargs)  -> SqlAlchemyModel:
    """
    Does a database select, based of of the query data provided, returns the
    first object in the result set.

    Raises a 404 if data can not be found.
    """
    # Get query only takes PKs, no kwargs. Filter however is more flexible.
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    return instance


def update_entry(model: typing.Type[SqlAlchemyModel], **kwargs) -> SqlAlchemyModel:
    """
    Does a database select, based of of the query data provided, readies up an
    instance of the specific model based on the result data.
    Instance is then altered with the new data and saved to the database.

    Raises a 404 if initial data can not be found.
    """
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    for key, value in kwargs["data"].items():
        setattr(instance, key, value)
    db.session.commit()
    return instance


def delete_entry(model: typing.Type[SqlAlchemyModel], **kwargs) -> None:
    """
    Does a database select, based of of the query data provided, readies up an
    instance of the specific model based on the result data.
    Instance is then passed as parameter for deletion.

    Raises a 404 if initial data can not be found.
    """
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    db.session.delete(instance)
    db.session.commit()


def list_entry(model: typing.Type[SqlAlchemyModel], **kwargs) -> typing.List[SqlAlchemyModel]:
    """
    Builds a SQLAlchemy query up from incoming kwargs.

    Finally returns a list of SQLAlchemy model instances.
    """
    query = model.query
    ids = kwargs["query"].get("ids")
    if ids:
        # Need to do some more work to handle composite PKs. Pass the set of
        # ids in a dictionary.
        if isinstance(ids, dict):
            # Unpack the dictionary and only do some work if the value is not
            # None. No sense in passing another filter value if it has to do
            # nothing.
            for key, id in ids.items():
                if id != None:
                    query = query.filter(
                        getattr(model, key)==id
                    )
        else:
            query = query.filter(model.id.in_(ids))

    # Append order by
    # NOTE: order_by(SqlAlchemyModel.column, SqlAlchemyModel.column ...) is
    # equal to order_by(SqlAlchemyModel.column).order_by(
    # SqlAlchemyModel.column)...
    for column in  kwargs["query"]["order_by"]:
        query = query.order_by(getattr(model, column))
    return query.offset(
        kwargs["query"].get("offset", 0)
    ).limit(
        kwargs["query"].get("limit", settings.DEFAULT_API_LIMIT)
    ).all()


def transform(
        instance: typing.Union[SqlAlchemyModel, typing.List[SqlAlchemyModel]],
        api_model: typing.Type[ApiModel]) -> \
        typing.Union[ApiModel, typing.List[ApiModel]]:
    """
    Translate model object into a swagger API model instance or a list of
    swagger API model instances. To assist with json serialization later on in
    flask.

    :param instance: SQLAlchemy model instance
    :param api_model: Swagger API model class
    :return: Swagger API model instance
    :return: List[Swagger API model instance]
    """
    data = None
    if instance == None or instance == []:
        # TODO raise 404
        return None
    model_name = instance.__class__.__name__ \
        if not isinstance(instance, list) else instance[0].__class__.__name__
    transformer = getattr(mappings, "DB_TO_API_%s_TRANSFORMATION" % model_name.upper())

    # TODO look at instance.__dict__ later, seems to not always provide the
    # expected dict.
    if isinstance(instance, list):
        data = []
        for obj in instance:
            obj_data = {}
            for key in obj.__table__.columns.keys():
                obj_data[key] = getattr(obj, key)
            data.append(
                api_model.from_dict(transformer.apply(obj_data))
            )
    else:
        data = {}
        for key in instance.__table__.columns.keys():
            data[key] = getattr(instance, key)
        data = api_model.from_dict(transformer.apply(data))
    return data
