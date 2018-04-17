from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from project import settings

APP = Flask(__name__)
SENTRY = Sentry(dsn=settings.SENTRY_DSN)

APP.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialise sentry
SENTRY.init_app(APP, level=settings.SENTRY_LOG_LEVEL)

DB = SQLAlchemy(APP)
