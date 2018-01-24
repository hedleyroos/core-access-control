from flask import jsonify

from . import models
from .models import DB as db


# NOTE Actions will need error handling in the long run. However a KeyError is better
# than no error at this stage,
def crud(model, action, data=None, query=None):
    model = getattr(models, model)
    return serializer(globals()["%s_entry" % action](
        model=model,
        **{"data": data, "query": query}
    ))


def create_entry(model, **kwargs):
    instance = model(**kwargs["data"])
    db.session.add(instance)
    db.session.commit()
    return instance


def read_entry(model, **kwargs):
    # Get query only takes PKs, no kwargs. Filter however is more flexible.
    instance = model.query.filter_by(**kwargs["query"]).first_or_404()
    return instance


def update_entry(model, **kwargs):
    instance = model.query.get(**kwargs["query"])
    for key, value in kwargs["data"]:
        setattr(instance, key, value)
    db.session.commit()
    return instance


def delete_entry(model, **kwargs):
    # Can not safely without explicit select on id.
    instance = model.query.get(kwargs["query"]["id"])
    db.session.delete(instance)
    db.session.commit()


def list_entry(model, **kwargs):
    query = None
    if kwargs["query"].get("ids"):
        query = model.query.filter(model.id.in_(query["ids"]))
    else:
        query = model.query
    return query.offset(
        kwargs["query"].get("offet", None)
    ).limit(
        kwargs["query"].get("limit", None)
    ).all()


def serializer(instance):
    """
    Translate model object into a dictionary, to assist with json
    serialization.

    :param instance: SQLAlchemy model instance
    :return: python dict
    """
    data = None
    if isinstance(instance, list):
        data = []
        for obj in instance:
            obj_data = {}
            for key in obj.__table__.columns.keys():
                obj_data[key] = getattr(obj, key)
            data.append(obj_data)
    else:
        data = {}
        for key in instance.__table__.columns.keys():
            data[key] = getattr(instance, key)

    return data
