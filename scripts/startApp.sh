#!/bin/bash

python manage.py db upgrade -d access_control/migrations
# TODO: Disabled running uwsgi since it caused issues in the docker-compose
# environment. Will re-enabled when I figure out how to let uwsgi keep connections
# open.
# uwsgi uwsgi.ini
python3 -m swagger_server
