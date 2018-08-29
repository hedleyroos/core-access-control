import random
import uuid
from datetime import datetime

import werkzeug

from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.models import Domain
from swagger_server.models import DomainRole
from swagger_server.models import Role
from swagger_server.models import Invitation
from swagger_server.models import InvitationDomainRole
from swagger_server.models import InvitationDomainRoleCreate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationDomainRoleTestCase(BaseTestCase):

    @decorators._db_exception
    def setUp(self):
        super().setUp()
        self.role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "invitation_site_role to create",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )
        self.domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test domain",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_data,
            action="create"
        )

        self.domain_role_data = {
            "role_id": self.role_model.id,
            "domain_id": self.domain_model.id
        }
        self.domain_role_model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=self.domain_role_data,
            action="create"
        )
        self.invitation_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "invitationdomainrole@test.com",
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

    def test_invitationdomainrole_create(self):
        data = InvitationDomainRoleCreate(**{
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        })
        response = self.client.open(
            '/api/v1/invitationdomainroles',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["domain_id"], data.domain_id)

    def test_invitationdomainrole_delete(self):
        data = {
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        }
        invitation_domain_role = db_actions.crud(
            model="InvitationDomainRole",
            api_model=InvitationDomainRole,
            data=data,
            action="create"
        )

        with self.assertRaises(werkzeug.exceptions.NotFound):
            response = self.client.open(
                '/api/v1/invitationdomainroles/{invitation_id}/{domain_id}/{role_id}'.format(
                    invitation_id=invitation_domain_role.invitation_id,
                    domain_id=invitation_domain_role.domain_id,
                    role_id=invitation_domain_role.role_id,
                ),
                method='DELETE',
                headers=self.headers)

            db_actions.crud(
                model="InvitationDomainRole",
                api_model=InvitationDomainRole,
                action="read",
                query={
                    "role_id": invitation_domain_role.role_id,
                    "domain_id": invitation_domain_role.domain_id,
                    "invitation_id": invitation_domain_role.invitation_id
                }
            )

    def test_invitationdomainrole_read(self):
        data = {
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        }
        invitation_domain_role = db_actions.crud(
            model="InvitationDomainRole",
            api_model=InvitationDomainRole,
            data=data,
            action="create"
        )

        response = self.client.open(
            '/api/v1/invitationdomainroles/{invitation_id}/{domain_id}/{role_id}'.format(
                invitation_id=invitation_domain_role.invitation_id,
                domain_id=invitation_domain_role.domain_id,
                role_id=invitation_domain_role.role_id,
            ),
            method='GET',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], invitation_domain_role.role_id)
        self.assertEqual(r_data["domain_id"], invitation_domain_role.domain_id)

    def test_invitationdomainrole_list(self):
        objects = []
        num_entries = random.randint(5, 20)
        for index in range(1, num_entries):
            role_data = {
                "label": ("%s" % uuid.uuid4())[:30],
                "description": "invitation_site_role to create",
            }
            role_model = db_actions.crud(
                model="Role",
                api_model=Role,
                data=role_data,
                action="create"
            )
            domain_role_data = {
                "role_id": role_model.id,
                "domain_id": self.domain_model.id
            }
            domain_role_model = db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data=domain_role_data,
                action="create"
            )
            invitation_domain_role_data = {
                "role_id": role_model.id,
                "domain_id": self.domain_model.id,
                "invitation_id": self.invitation_model.id
            }
            objects.append(db_actions.crud(
                model="InvitationDomainRole",
                api_model=InvitationDomainRole,
                data=invitation_domain_role_data,
                action="create"
            ))

        query_string = [
            ("limit", 2),
            ("invitation_id", self.invitation_model.id)
        ]
        response = self.client.open(
            '/api/v1/invitationdomainroles',
            method='GET',
            query_string=query_string,
            headers=self.headers)

        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
