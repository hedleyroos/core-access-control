#!/usr/bin/env python3

import connexion

from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from project import settings
from project.errors import errors
from sqlalchemy.exc import SQLAlchemyError
from ge_core_shared import exception_handlers, middleware

from swagger_server import encoder

DB = SQLAlchemy()
SENTRY = Sentry(dsn=settings.SENTRY_DSN)

# We create and set up the app variable in the global context as it is used by uwsgi.
app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Access Control API'})

app.app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)
app.app.wsgi_app = middleware.AuthMiddleware(app.app.wsgi_app)
app.app.register_blueprint(errors)

DB.init_app(app.app)
SENTRY.init_app(app.app, level=settings.SENTRY_LOG_LEVEL)


if __name__ == '__main__':
    app.run(port=8080)
