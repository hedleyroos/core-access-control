import os

from project.app import DB

DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)
API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))


# Late import due to circular import issues.
from access_control import models, mappings

# core shared settings
SQLALCHEMY_DB = DB
ACTION_MODELS = models
ACTION_MAPPINGS = mappings

