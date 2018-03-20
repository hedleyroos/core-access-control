import os

DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
DB_URI = os.environ.get(
    "DB_URI",
    "postgres+psycopg2://access_control:password@localhost:5432/access_control"
)

API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))
