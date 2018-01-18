import os

from flask import Flask

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from settings import settings


APP = Flask(__name__)

# TODO Move to settings and make env driven.
APP.config["SQLALCHEMY_DATABASE_URI"] = "postgres+psycopg2://core-access-control:core-access-control@localhost:5432/core-access-control"
    #os.environ.get(
DB = SQLAlchemy(APP)
migrate = Migrate(APP, DB)


class Role(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.String(80))
    description = DB.Column(DB.String(80))
    requires_2fa = DB.Column(DB.Boolean())

    def __repr__(self):
        return "String"
