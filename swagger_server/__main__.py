#!/usr/bin/env python3

import connexion

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from access_control import models

from swagger_server import encoder, exception_handlers, middleware

DB = SQLAlchemy()

# We create and set up the app variable in the global context as it is used by uwsgi.
app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Access Control API'})
app.app.config = models.APP.config
DB.init_app(app.app)
app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)
app.app.wsgi_app = middleware.AuthMiddleware(app.app.wsgi_app)

if __name__ == '__main__':
    app.run(port=8080)
