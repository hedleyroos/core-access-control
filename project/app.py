import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from project import settings


APP = Flask(__name__)
SENTRY = Sentry(dsn=settings.SENTRY_DSN)

# Grab URI from env here, instead of getting it from settings. Original setting
# implementation caused circular import issues for certain envs. Tox test env
# for example.
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)
APP.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise sentry
SENTRY.init_app(APP, level=settings.SENTRY_LOG_LEVEL)

DB = SQLAlchemy(APP)
