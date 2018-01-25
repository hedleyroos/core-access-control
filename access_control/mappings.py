from .transformation import Transformation, Mapping
from werkzeug.http import http_date

def datetime_to_string(date):
    return http_date(date.timetuple())

DB_TO_API_DOMAIN_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "name", "description", "parent_id"
    ]
)
