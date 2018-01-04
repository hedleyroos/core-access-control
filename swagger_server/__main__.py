#!/usr/bin/env python3

import connexion
from .encoder import JSONEncoder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': '# The Access Control API  ## Overview The Access Control API is an API exposed to other core components. It uses an API Key in an HTTP header to perform authentication and authorisation.  Most of the API calls facilitates CRUD of the entities defined in the Access Control component. Others calls allows the retrieval of information in a form that is convenient for other components (most notably the Management Layer) to consume. '})
    app.run(port=8080)
