import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)

# Grab URI from env here, instead of getting it from settings. Original setting
# implementation caused circular import issues for certain envs. Tox test env
# for example.
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)
APP.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

DB = SQLAlchemy(APP)
