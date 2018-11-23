import datetime
import os

import connexion

import project.app

orig_environ = dict(os.environ)
orig_environ["ALLOWED_API_KEYS"] = "test-api-key"
os.environ.update(orig_environ)

from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from sqlalchemy.exc import SQLAlchemyError
from ge_core_shared import decorators, exception_handlers, middleware

from swagger_server.encoder import JSONEncoder
from access_control import models


DB = SQLAlchemy()


def mangle_data(model, data):
    """
    Mass update for certain models' data that have had definition changes,
    primarily changes in non nullable fields, since original test creation and
    make use of db_create_entry.

    """
    if model.lower() == "site":
        if not data.get("deletion_method_id"):
            data["deletion_method_id"] = 0
    return data


def db_create_entry(model, **kwargs):
    """
    Helper method for unit tests, creation during testing tends to bypass the
    actual api endpoints. The resulting Api models from using the core_shared
    crud create, is sometimes missing attributes needed to make testing easier.
    """
    data = mangle_data(model, kwargs["data"])
    model = getattr(models, model)
    instance = model(**data)
    DB.session.add(instance)
    DB.session.commit()
    return instance


class BaseTestCase(TestCase):

    def create_app(self):
        app = connexion.App(__name__, specification_dir='../swagger/')
        flask_app = app.app
        flask_app.json_encoder = JSONEncoder
        flask_app.config = project.app.APP.config
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        DB.init_app(flask_app)
        app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)

        # Register middleware
        middleware.auth_middleware(flask_app, "core_access_control")
        app.add_api('swagger.yaml', arguments={'title': 'Test Access Control API'})
        return flask_app

    @decorators.db_exception
    def setUp(self):
        super().setUp()
        meta = DB.metadata
        meta.reflect(DB.engine)

        # By reversing the tables, children should get deleted before parents.
        for table in reversed(meta.sorted_tables):
            if table.name == "alembic_version":  # Do not delete migration data
                continue

            DB.session.execute(table.delete())
        DB.session.commit()

        # LOAD FIXTURES FOUND ONLY IN DATA MIGRATIONS
        for model, data in data_migration.DATA.items():
            # NOTE: Seemingly only raw SQL executes work in the test setUp.
            DB.session.execute(
                "INSERT INTO deletion_method (id, label, data_schema, description, created_at, updated_at)"
                " VALUES ('0', 'none', '{\"type\": \"object\", \"additionalProperties\": false, \"properties\": {}}',"
                f" 'None type method', '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}', '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}');"
            )

    def tearDown(self):
        super().tearDown()
        # Closes all active connections between tests. Prevents session errors
        # bleeding over.
        DB.session.close_all()
