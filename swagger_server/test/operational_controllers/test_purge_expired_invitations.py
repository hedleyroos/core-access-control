import json
import uuid

import werkzeug
from datetime import datetime, timedelta
from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.models import Domain
from swagger_server.models import DomainRole
from swagger_server.models import Invitation
from swagger_server.models import InvitationDomainRole
from swagger_server.models import InvitationSiteRole
from swagger_server.models import Role
from swagger_server.models import Site
from swagger_server.models import SiteRole
from swagger_server.test import BaseTestCase


class InvitationTestCase(BaseTestCase):

    @decorators.db_exception
    def setUp(self):
        super().setUp()
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "invitation_site_role to create"
        }
        self.role_model_1 = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "invitation_site_role to create"
        }
        self.role_model_2 = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test domain",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test domain 2"
        }
        self.domain_model_2 = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
        domain_role_data = {
            "role_id": self.role_model_1.id,
            "domain_id": self.domain_model.id
        }
        self.domain_role_model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=domain_role_data,
            action="create"
        )
        site_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test site",
            "domain_id": self.domain_model_2.id
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=site_data,
            action="create"
        )
        site_role_data = {
            "role_id": self.role_model_1.id,
            "site_id": self.site_model.id
        }
        self.site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=site_role_data,
            action="create"
        )
        site_role_data = {
            "role_id": self.role_model_2.id,
            "site_id": self.site_model.id
        }
        self.site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=site_role_data,
            action="create"
        )
        expired_invite_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "3firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now() - timedelta(days=1)
        }
        self.expired_invitation_model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=expired_invite_data,
            action="create"
        )
        invitation_domain_role_data = {
            "invitation_id": self.expired_invitation_model.id,
            "domain_id": self.domain_model.id,
            "role_id": self.role_model_1.id
        }
        self.invitation_domain_role_model = db_actions.crud(
            model="InvitationDomainRole",
            api_model=InvitationDomainRole,
            data=invitation_domain_role_data,
            action="create"
        )
        invitation_site_role_data = {
            "invitation_id": self.expired_invitation_model.id,
            "site_id": self.site_model.id,
            "role_id": self.role_model_1.id
        }
        self.invitation_site_role_model = db_actions.crud(
            model="InvitationSiteRole",
            api_model=InvitationSiteRole,
            data=invitation_site_role_data,
            action="create"
        )
        invitation_site_role_data = {
            "invitation_id": self.expired_invitation_model.id,
            "site_id": self.site_model.id,
            "role_id": self.role_model_2.id
        }
        self.invitation_site_role_model = db_actions.crud(
            model="InvitationSiteRole",
            api_model=InvitationSiteRole,
            data=invitation_site_role_data,
            action="create"
        )
        invite_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "7firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now()
        }
        self.invitation_model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=invite_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_purge_invitations_today(self):
        response = self.client.open(
            "/api/v1/ops/purge_expired_invitations",
            method='GET', headers=self.headers
        )
        r_data = json.loads(response.data)
        self.assertEqual(r_data["amount"], 1)
        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Invitation",
                api_model=Invitation,
                action="read",
                query={"id": self.expired_invitation_model.id}
            )

    def test_purge_invitations_cutoff_date(self):
        response = self.client.open(
            "/api/v1/ops/purge_expired_invitations",
            method='GET',
            query_string=[
                ("cutoff_date", (datetime.now() + timedelta(days=1)).date())
            ],
            headers=self.headers
        )
        r_data = json.loads(response.data)
        self.assertEqual(r_data["amount"], 2)
        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Invitation",
                api_model=Invitation,
                action="read",
                query={"id": self.expired_invitation_model.id}
            )
        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Invitation",
                api_model=Invitation,
                action="read",
                query={"id": self.invitation_model.id}
            )
