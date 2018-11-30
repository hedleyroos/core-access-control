import jsonschema
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from access_control.models import (DeletionMethod, Site)


# Exceptions and handlers
class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
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
            raise InvalidRequest(f"No result found for: DeletionMethod<id={lookup_id}>")
        try:
            jsonschema.validate(
                data,
                schema=deletion_method.data_schema,
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError:
            raise InvalidRequest(
                f"deletion_method_data validation failed against schema: {deletion_method.data_schema}"
            )

    def validate_site_deletion_method_required_fields(self, lookup_id, data):
        has_data = data or data == {}
        if has_data and not lookup_id >= 0:
            raise InvalidRequest("deletion_method_id is required if deletion_method_data is provided")
        elif lookup_id >= 0 and not has_data:
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
            raise InvalidRequest(f"No result found for: Site<id={lookup_id}>")
        method_id = data.get("deletion_method_id") or site.deletion_method_id
        method_data = data.get("deletion_method_data") or site.deletion_method_data
        self.validate_site_deletion_method_required_fields(
            method_id, method_data
        )
        self.validate_site_deletion_method_data(
            method_id, method_data
        )
