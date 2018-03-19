import uuid

import os

from unittest.mock import patch

# with patch.dict(os.environ, {
#     "ALLOWED_API_KEYS": "ahjaeK1thee9aixuogho"
# }):
#     from swagger_server import middleware

from access_control import db_actions
from swagger_server.models import Domain
from swagger_server.test import BaseTestCase


class AuthenticationTestCase(BaseTestCase):

    def setUp(self):
        self.domain_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test domain",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_data,
            action="create"
        )

        self.headers = {"X-API-KEY": "test-api-key"}

    @patch.dict(os.environ, {
        "ALLOWED_API_KEYS": "ahjaeK1thee9aixuogho"
    })
    def test_unauthorized(self):
        response = self.client.open(
            "/api/v1/domains/{domain_id}".format(
                domain_id=self.domain_model.id
            ),
            method='GET'
        )
        self.assert401(response)

    def test_wrong_key(self):
        response = self.client.open(
            "/api/v1/domains/{domain_id}".format(
                domain_id=self.domain_model.id
            ),
            method='GET',
            headers={"X-API-KEY": "qwerty"}
        )
        self.assert401(response)

    def test_authorized(self):
        response = self.client.open(
            "/api/v1/domains/{domain_id}".format(
                domain_id=self.domain_model.id
            ),
            method='GET',
            headers=self.headers
        )
        self.assert200(response)
