#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_sqlalchemy import SQLAlchemy

from access_control import models

DB = SQLAlchemy()

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Access Control API'})
    app.app.config = models.APP.config
    DB.init_app(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
