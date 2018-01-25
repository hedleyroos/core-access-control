import typing

from flask import jsonify

from . import mappings
from . import models
from . import settings
from .models import DB as db

ApiModel = typing.TypeVar("ApiModel")
SqlAlchemyModel = typing.TypeVar("SqlAlchemyModel")


# NOTE Actions will need error handling in the long run. However a KeyError is better
# than no error at this stage,
def crud(
        model: SqlAlchemyModel,
        api_model: ApiModel,
        action: str,
        data: dict = None,
        query: dict = None) -> typing.Union[ApiModel, typing.List[ApiModel]]:
    model = getattr(models, model)
    return transform(
        globals()["%s_entry" % action](
            model=model,
            **{"data": data, "query": query}
        ),
        api_model=api_model
    )


def create_entry(model: SqlAlchemyModel, **kwargs) -> SqlAlchemyModel:
    instance = model(**kwargs["data"])
    db.session.add(instance)
    db.session.commit()
    return instance


def read_entry(model: SqlAlchemyModel, **kwargs)  -> SqlAlchemyModel:
    # Get query only takes PKs, no kwargs. Filter however is more flexible.
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    return instance


def update_entry(model: SqlAlchemyModel, **kwargs) -> SqlAlchemyModel:
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    for key, value in kwargs["data"].items():
        setattr(instance, key, value)
    db.session.commit()
    return instance


def delete_entry(model: SqlAlchemyModel, **kwargs) -> SqlAlchemyModel:
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    db.session.delete(instance)
    db.session.commit()


def list_entry(model: SqlAlchemyModel, **kwargs) -> typing.List[SqlAlchemyModel]:
    query = model.query
    if kwargs["query"].get("ids"):
        query = query.filter(model.id.in_(kwargs["query"].get("ids")))

    # Append order by
    # NOTE: order_by(SqlAlchemyModel.column, SqlAlchemyModel.column ...) is
    # equal to order_by(SqlAlchemyModel.column).order_by(
    # SqlAlchemyModel.column)...
    for column in  kwargs["query"]["order_by"]:
        query = query.order_by(getattr(model, column))
    return query.offset(
        kwargs["query"].get("offet", 0)
    ).limit(
        kwargs["query"].get("limit", settings.DEFAULT_API_LIMIT)
    ).all()


def transform(instance: SqlAlchemyModel, api_model: ApiModel) -> \
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
