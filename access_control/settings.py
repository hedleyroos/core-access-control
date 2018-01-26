import os

DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://core_access_control" \
    ":core_access_control@localhost:5432/core-access-control"
)
