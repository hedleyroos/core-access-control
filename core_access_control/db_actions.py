from flask import jsonify

from . import models
from .models import DB as db

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
    instance = db.session.query(model).get(kwargs["query"]["id"])
    return instance


def update_entry(model, **kwargs):
    instance = model.query.get(**kwargs["query"])
    for key, value in kwargs["data"]:
        setattr(instance, key, value)
    db.session.commit()
    return instance


def delete_entry(model, **kwargs):
    instance = model.query.get(**kwargs["query"])
    db.session.delete(instance)
    db.session.commit()

    # TODO decide what to return.
    return None


def list_entry(model, **kwargs):
    model.query.all()
    db.session.query(model)
    db.session.commit()

def serializer(instance):
    data = {}
    for prop in instance.__mapper__.iterate_properties:
        data[prop.key] = getattr(instance, prop.key)

    return data
