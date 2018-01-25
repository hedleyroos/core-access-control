import datetime

from .transformation import Transformation, Mapping

def datetime_to_string(date):
    """
    :param date: Timezone unaware datetime object
    :return str: RFC 3339 format datetime string
    """
    return date.astimezone(datetime.timezone.utc).isoformat()

DB_TO_API_DOMAIN_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "name", "description", "parent_id"
    ]
)
