import uuid

from swagger_server.models import InvitationCreate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationTestCase(BaseTestCase):

    def test_invitiation_create(self):
        data = InvitationCreate(**{
            "first_name": "first",
            "last_name": "last",
            "email": "first.last@test.com",
            "invitor_id": "%s" % uuid.uuid4()
        })
        response = self.client.open(
            '/api/v1/invitations/',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["first_name"], data.first_name)
        self.assertEqual(r_data["last_name"], data.last_name)