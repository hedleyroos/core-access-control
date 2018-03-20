from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from project.settings import DB_URI

APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

DB = SQLAlchemy(APP)