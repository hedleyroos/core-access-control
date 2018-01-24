from flask import jsonify

from core_access_control import models
from core_access_control.models import DB as db

def crud(model, action, data=None, query=None):
    model = getattr(models, model)
    return globals()["%s_entry" % action](
        model=model,
        **{"data": data, "query": query}
    )


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
    for key, val in instance.__dict__.items():
        try:
            data[key] = jsonify(val)
        except TypeError as e:
            print (e)

    return data
