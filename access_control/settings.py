import os

DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://core-access-control" \
    ":core-access-control@localhost:5432/core-access-control"
)
