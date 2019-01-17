import jsonschema
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from access_control.models import (DeletionMethod, Site)


# Exceptions and handlers
class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def handle_invalid_request(error):
    # Can be reused for most Exceptions
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# Validators
class SiteValidator:

    def validate_site_deletion_method_data(self, lookup_id, data):
        try:
            deletion_method = DeletionMethod.query.filter_by(
                id=lookup_id
            ).one()
        except NoResultFound:
            raise InvalidRequest(f"Deletion method with ID {lookup_id} does not exist")
        try:
            jsonschema.validate(
                data,
                schema=deletion_method.data_schema,
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError:
            raise InvalidRequest(
                "The deletion method data does not conform to the"
                f" schema defined for the deletion method {deletion_method.label}"
            )

    def validate_site_deletion_method_required_fields(self, lookup_id, data):
        if data is not None and lookup_id is None:
            raise InvalidRequest("deletion_method_id is required if deletion_method_data is provided")
        elif lookup_id is not None and data is None:
            raise InvalidRequest("deletion_method_data is required if deletion_method_id is provided")

    def validate_site_create(self, data):
        method_id = data.get("deletion_method_id")
        method_data = data.get("deletion_method_data")
        self.validate_site_deletion_method_required_fields(
            method_id, method_data
        )
        self.validate_site_deletion_method_data(
            method_id, method_data
        )

    def validate_site_update(self, lookup_id, data):
        try:
            site = Site.query.filter_by(id=lookup_id).one()
        except NoResultFound:
            raise InvalidRequest(f"Site with ID {lookup_id} does not exist")
        method_id = data.get("deletion_method_id") or site.deletion_method_id
        method_data = data.get("deletion_method_data") or site.deletion_method_data
        self.validate_site_deletion_method_required_fields(
            method_id, method_data
        )
        self.validate_site_deletion_method_data(
            method_id, method_data
        )
