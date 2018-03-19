import uuid

import os

from unittest.mock import patch


from access_control import db_actions
from access_control.settings import API_KEY_HEADER
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

        self.headers = {API_KEY_HEADER: "test-api-key"}

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
            headers={API_KEY_HEADER: "qwerty"}
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
