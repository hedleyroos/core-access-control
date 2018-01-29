import uuid

from datetime import datetime

from swagger_server.models import InvitationCreate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationTestCase(BaseTestCase):

    def test_invitiation_create(self):
        data = InvitationCreate(**{
            "first_name": "first",
            "last_name": "last",
            "email": "0firstlast@test.com",
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        })
        response = self.client.open(
            '/api/v1/invitations/',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["first_name"], data.first_name)
        self.assertEqual(r_data["last_name"], data.last_name)
        self.assertEqual(r_data["email"], data.email)
        self.assertEqual(r_data["invitor_id"], data.invitor_id)

    def test_invitation_read(self):
        pass

    def test_invitation_list(self):
        pass

    def test_invitation_update(self):
        pass

    def test_invitation_redeem(self):
        pass
