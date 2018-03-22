import importlib
import os

from access_control import mappings, models
import project.app


DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))

# core shared settings
SQLALCHEMY_DB = project.app.DB
ACTION_MODELS = models
ACTION_MAPPINGS = mappings
