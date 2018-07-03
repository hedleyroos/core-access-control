import random
import uuid
from datetime import datetime

import werkzeug

from ge_core_shared import db_actions

from access_control import models
from project.settings import API_KEY_HEADER
from swagger_server.models import Site, Domain
from swagger_server.models import SiteRole
from swagger_server.models import Role
from swagger_server.models import Invitation
from swagger_server.models import InvitationSiteRole
from swagger_server.models import InvitationSiteRoleCreate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationSiteRoleTestCase(BaseTestCase):

    def setUp(self):
        models.InvitationSiteRole.query.delete()
        models.InvitationDomainRole.query.delete()
        models.Invitation.query.delete()
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
        self.site_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test site",
            "domain_id": self.domain_model.id
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )

        self.site_role_data = {
            "role_id": self.role_model.id,
            "site_id": self.site_model.id
        }
        self.site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=self.site_role_data,
            action="create"
        )
        self.invitation_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "invitationsiterole@test.com",
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

    def test_invitationsiterole_create(self):
        data = InvitationSiteRoleCreate(**{
            "site_id": self.site_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        })
        response = self.client.open(
            '/api/v1/invitationsiteroles',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["site_id"], data.site_id)

    def test_invitationsiterole_delete(self):
        data = {
            "site_id": self.site_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        }
        invitation_site_role = db_actions.crud(
            model="InvitationSiteRole",
            api_model=InvitationSiteRole,
            data=data,
            action="create"
        )

        with self.assertRaises(werkzeug.exceptions.NotFound):
            response = self.client.open(
                '/api/v1/invitationsiteroles/{invitation_id}/{site_id}/{role_id}'.format(
                    invitation_id=invitation_site_role.invitation_id,
                    site_id=invitation_site_role.site_id,
                    role_id=invitation_site_role.role_id,
                ),
                method='DELETE',
                headers=self.headers)

            db_actions.crud(
                model="InvitationSiteRole",
                api_model=InvitationSiteRole,
                action="read",
                query={
                    "role_id": invitation_site_role.role_id,
                    "site_id": invitation_site_role.site_id,
                    "invitation_id": invitation_site_role.invitation_id
                }
            )

    def test_invitationsiterole_read(self):
        data = {
            "site_id": self.site_model.id,
            "role_id": self.role_model.id,
            "invitation_id": self.invitation_model.id
        }
        invitation_site_role = db_actions.crud(
            model="InvitationSiteRole",
            api_model=InvitationSiteRole,
            data=data,
            action="create"
        )

        response = self.client.open(
            '/api/v1/invitationsiteroles/{invitation_id}/{site_id}/{role_id}'.format(
                invitation_id=invitation_site_role.invitation_id,
                site_id=invitation_site_role.site_id,
                role_id=invitation_site_role.role_id,
            ),
            method='GET',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], invitation_site_role.role_id)
        self.assertEqual(r_data["site_id"], invitation_site_role.site_id)

    def test_invitationsiterole_list(self):
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
            site_role_data = {
                "role_id": role_model.id,
                "site_id": self.site_model.id
            }
            site_role_model = db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data=site_role_data,
                action="create"
            )
            invitation_site_role_data = {
                "role_id": role_model.id,
                "site_id": self.site_model.id,
                "invitation_id": self.invitation_model.id
            }
            objects.append(db_actions.crud(
                model="InvitationSiteRole",
                api_model=InvitationSiteRole,
                data=invitation_site_role_data,
                action="create"
            ))

        query_string = [
            ("limit", 2),
            ("invitation_id", self.invitation_model.id)
        ]
        response = self.client.open(
            '/api/v1/invitationsiteroles',
            method='GET',
            query_string=query_string,
            headers=self.headers)

        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
