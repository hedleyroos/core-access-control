import logging

import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder

from core_access_control import models

DB = SQLAlchemy()


class BaseTestCase(TestCase):

    def create_app(self):
        #logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.app.config = models.APP.config
        app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        DB.init_app(app.app)
        app.add_api('swagger.yaml', arguments={'title': 'Test Access Control API'})
        return app.app
