DELETION_METHODS = [
    {
        "label": "none",
        "data_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {}
        },
        "description": "None type method"
    },
    {
        "label": "email",
        "data_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "recipients": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "email"
                    }
                }
            },
            "required": [
                "recipients"
            ]
        },
        "description": "Schema for the email deletion method"
    },
    {
        "label": "api",
        "data_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "headers": {
                    "type": "string",
                },
                "body": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "format": "uuid"
                        }
                    },
                    "required": [
                        "user_id"
                    ]
                }
            },
            "required": [
                "body"
            ]
        },
        "description": "Schema for the email deletion method"
    }
]
