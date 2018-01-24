import os

from flask import Flask, request, jsonify

from . import db_actions

from .models import APP as app

@app.route("/domain/<id>", methods=["GET"])
def user_detail(id):
    instance =  db_actions.crud(
        model="Domain",
        action="read",
        query={"id": id}
    )
    return jsonify(instance)
