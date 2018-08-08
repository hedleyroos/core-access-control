import uuid

from jsonschema import FormatChecker


@FormatChecker.cls_checks("uuid")
def check_uuid_format(instance):
    try:
        uuid.UUID(instance)
        return True
    except ValueError:
        return False


print("JSONSchema validation supported for the following 'format' values:")
print(", ".join(FormatChecker.checkers.keys()))
