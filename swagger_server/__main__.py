#!/usr/bin/env python3

import connexion

from swagger_server import encoder

from core_access_control import models

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app = models.APP
    app.add_api('swagger.yaml', arguments={'title': 'Access Control API'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
