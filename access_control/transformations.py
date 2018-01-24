NOTIFICATION_TRANSFORMATION = Transformation(
    mappings=[
        Mapping(input_field="created_date", conversion=datetime_to_string),
        Mapping(input_field="sent_date", conversion=datetime_to_string)
    ],
    copy_fields=[
        "id", "description", "sent", "policy_holder_id"
    ]
)
