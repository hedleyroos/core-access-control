#!/bin/bash

python manage.py db upgrade -d access_control/migrations
uwsgi uwsgi.ini
