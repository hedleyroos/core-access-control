import datetime

from .transformation import Transformation, Mapping

def datetime_to_string(date):
    """
    :param date: Timezone unaware datetime object
    :return str: Python iso formatted string
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

DB_TO_API_ROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "label", "description", "requires_2fa"
    ]
)

DB_TO_API_PERMISSION_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "name", "description"
    ]
)

DB_TO_API_RESOURCE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "urn", "description"
    ]
)

DB_TO_API_ROLERESOURCEPERMISSION_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "role_id", "resource_id", "permission_id"
    ]
)

DB_TO_API_SITE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "name", "domain_id", "description", "client_id", "is_active"
    ]
)
