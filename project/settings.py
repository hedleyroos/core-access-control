import logging
import os


INVITATION_EXPIRY_DAYS = int(os.environ.get("INVITATION_EXPIRY_DAYS", 5))
DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))
UNPROTECTED_API_ENDPOINTS = {
    "/api/v1/ops/healthcheck",
    "/metrics"
}

# core shared settings
ACTION_MODELS = "access_control.models"
ACTION_MAPPINGS = "access_control.mappings"

# sentry settings
SENTRY_DSN = os.environ.get("SENTRY_DSN", None)
SENTRY_LOG_LEVEL = os.environ.get("SENTRY_LOG_LEVEL", logging.ERROR)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)
SQLALCHEMY_TRACK_MODIFICATIONS = \
    os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "false").lower() == "true"
