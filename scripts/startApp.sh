#!/bin/bash

FLASK_APP=access_control/models.py flask db upgrade -d access_control/migrations
python3 -m swagger_server
