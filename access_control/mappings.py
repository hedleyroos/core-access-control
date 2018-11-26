import datetime

from ge_core_shared.transformation import Transformation, Mapping


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
        "id", "name", "domain_id", "description", "client_id", "is_active",
        "deletion_method_id", "deletion_method_data"
    ]
)

DB_TO_API_CREDENTIALS_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "site_id", "account_id", "account_secret", "description"
    ]
)

DB_TO_API_DOMAINROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "domain_id", "role_id", "grant_implicitly",
    ]
)

DB_TO_API_SITEROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string)
    ],
    copy_fields=[
        "site_id", "role_id", "grant_implicitly",
    ]
)

DB_TO_API_USERSITEROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "site_id", "role_id", "user_id"
    ]
)

DB_TO_API_USERDOMAINROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "domain_id", "role_id", "user_id"
    ]
)

DB_TO_API_INVITATION_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
        Mapping(input_field="expires_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "id", "first_name", "last_name", "email", "invitor_id", "organisation_id",
        "invitation_redirect_url_id"
    ]
)

DB_TO_API_INVITATIONDOMAINROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "domain_id", "role_id", "invitation_id"
    ]
)

DB_TO_API_INVITATIONSITEROLE_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "site_id", "role_id", "invitation_id"
    ]
)

DB_TO_API_INVITATIONREDIRECTURL_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_at", conversion=datetime_to_string),
        Mapping(input_field="updated_at", conversion=datetime_to_string),
    ],
    copy_fields=[
        "id", "url", "description"
    ]
)
