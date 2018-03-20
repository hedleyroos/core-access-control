import importlib
import os

from access_control import mappings


DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)
API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))

# core shared settings
SQLALCHEMY_DB = getattr(importlib.import_module("project.app"), "DB")
ACTION_MODELS = importlib.import_module("access_control.models")
ACTION_MAPPINGS = mappings

