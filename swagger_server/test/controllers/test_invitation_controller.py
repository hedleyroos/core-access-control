import random
import uuid

from datetime import datetime
from time import strptime

import werkzeug
from ge_core_shared import db_actions

from access_control import models
from project.settings import API_KEY_HEADER
from swagger_server.models import Invitation
from swagger_server.models import InvitationCreate
from swagger_server.models import InvitationUpdate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationTestCase(BaseTestCase):

    def setUp(self):
        models.Invitation.query.delete()
        self.invitation_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "3firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        }
        self.invitation_model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=self.invitation_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_invitation_create(self):
        data = InvitationCreate(**{
            "first_name": "first",
            "last_name": "last",
            "email": "1firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        })
        response = self.client.open(
            '/api/v1/invitations',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        print(response)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["first_name"], data.first_name)
        self.assertEqual(r_data["last_name"], data.last_name)
        self.assertEqual(r_data["email"], data.email)
        self.assertEqual(r_data["organisation_id"], data.organisation_id)
        self.assertEqual(r_data["invitor_id"], data.invitor_id)

    def test_invitation_read(self):
        """Test case for invitation_read
        """
        response = self.client.open(
            '/api/v1/invitations/{invitation_id}'.format(invitation_id=self.invitation_model.id),
            method='GET', headers=self.headers)
        print(response)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["id"], self.invitation_model.id)
        self.assertEqual(r_data["first_name"], self.invitation_model.first_name)
        self.assertEqual(r_data["last_name"], self.invitation_model.last_name)
        self.assertEqual(r_data["email"], self.invitation_model.email)
        self.assertEqual(r_data["organisation_id"], self.invitation_model.organisation_id)
        self.assertEqual(r_data["invitor_id"], self.invitation_model.invitor_id)

    def test_invitation_delete(self):
        """Test case for invitation_delete
        """
        data = {
            "first_name": "first",
            "last_name": "last",
            "email": "2firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        }
        model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/invitations/{invitation_id}'.format(invitation_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Invitation",
                api_model=Invitation,
                action="read",
                query={"id": model.id}
            )

    def test_invitation_list(self):
        """Test case for invitation_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "first_name": "first",
                "last_name": "last",
                "email": f"test{index}@test.com",
                "organisation_id": 1,
                "invitor_id": "%s" % uuid.uuid1(),
                "expires_at": datetime.now()
            }
            objects.append(db_actions.crud(
                model="Invitation",
                api_model=Invitation,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
            ('invitation_ids', ",".join(map(str, [invitation.id for invitation in objects])))]
        response = self.client.open(
            '/api/v1/invitations',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        query_string = [('limit', 2),
                        ('invitation_ids', ",".join(map(str, [invitation.id for invitation in objects])))]
        response = self.client.open(
            '/api/v1/invitations',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))

    def test_invitation_update(self):
        """Test case for invitation_update
        """
        data = {
            "first_name": "first",
            "last_name": "last",
            "email": "update0@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        }
        model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=data,
            action="create"
        )
        data = {
            "first_name": "first",
            "last_name": "last",
            "email": "update1@test.com",
            "invitor_id": "%s" % uuid.uuid1(),
            "organisation_id": 2,
            "expires_at": datetime.now()
        }
        data = InvitationUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/invitations/{invitation_id}'.format(invitation_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["first_name"], updated_entry.first_name)
        self.assertEqual(r_data["last_name"], updated_entry.last_name)
        self.assertEqual(r_data["email"], updated_entry.email)
        self.assertEqual(r_data["invitor_id"], updated_entry.invitor_id)
        self.assertEqual(r_data["organisation_id"], updated_entry.organisation_id)
        self.assertEqual(r_data["expires_at"], updated_entry.expires_at.isoformat())

