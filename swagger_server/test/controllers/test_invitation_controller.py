import random
import uuid

from datetime import datetime, timedelta

import werkzeug
from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.models import Domain
from swagger_server.models import DomainRole
from swagger_server.models import Invitation
from swagger_server.models import InvitationRedirectUrl
from swagger_server.models import InvitationCreate
from swagger_server.models import InvitationDomainRole
from swagger_server.models import InvitationSiteRole
from swagger_server.models import InvitationUpdate
from swagger_server.models import Role
from swagger_server.models import Site
from swagger_server.models import SiteRole
from swagger_server.test import BaseTestCase
from flask import json


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
        invitation_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "3firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now() + timedelta(days=1)
        }
        self.invitation_model = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=invitation_data,
            action="create"
        )
        invitation_domain_role_data = {
            "invitation_id": self.invitation_model.id,
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
            "invitation_id": self.invitation_model.id,
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
            "invitation_id": self.invitation_model.id,
            "site_id": self.site_model.id,
            "role_id": self.role_model_2.id
        }
        self.invitation_site_role_model = db_actions.crud(
            model="InvitationSiteRole",
            api_model=InvitationSiteRole,
            data=invitation_site_role_data,
            action="create"
        )
        expired_invite_data = {
            "first_name": "first",
            "last_name": "last",
            "email": "7firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now() - timedelta(days=1)
        }
        self.expired_invite = db_actions.crud(
            model="Invitation",
            api_model=Invitation,
            data=expired_invite_data,
            action="create"
        )
        invitation_redirect_url_data = {
            "url": "http://example.com/redirect?foo=bar",
            "description": "A test redirect URL"
        }
        self.invitation_redirect_url = db_actions.crud(
            model="InvitationRedirectUrl",
            api_model=InvitationRedirectUrl,
            data=invitation_redirect_url_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_invitation_create(self):
        # Without redirect URL
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
        r_data = json.loads(response.data)
        self.assertEqual(r_data["first_name"], data.first_name)
        self.assertEqual(r_data["last_name"], data.last_name)
        self.assertEqual(r_data["email"], data.email)
        self.assertEqual(r_data["organisation_id"], data.organisation_id)
        self.assertEqual(r_data["invitor_id"], data.invitor_id)

        # With redirect URL
        data = InvitationCreate(**{
            "first_name": "first",
            "last_name": "last",
            "email": "2firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            "expires_at": datetime.now(),
            "invitation_redirect_url_id": self.invitation_redirect_url.id
        })
        response = self.client.open(
            '/api/v1/invitations',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["first_name"], data.first_name)
        self.assertEqual(r_data["last_name"], data.last_name)
        self.assertEqual(r_data["email"], data.email)
        self.assertEqual(r_data["organisation_id"], data.organisation_id)
        self.assertEqual(r_data["invitor_id"], data.invitor_id)
        self.assertEqual(r_data["invitation_redirect_url_id"],
                         data.invitation_redirect_url_id)

    def test_invitation_create_without_expiry(self):
        data = InvitationCreate(**{
            "first_name": "first",
            "last_name": "last",
            "email": "1firstlast@test.com",
            "organisation_id": 1,
            "invitor_id": "%s" % uuid.uuid1(),
            # No "expires_at" provided
        })
        response = self.client.open(
            '/api/v1/invitations',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
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

    def test_invitation_redeem(self):
        """Test Case for Redeeming of an Invitation
        """
        response = self.client.open(
            "/api/v1/invitations/{invitation_id}/redeem/{user_id}".format(
                invitation_id=self.invitation_model.id, user_id="%s" % uuid.uuid1()
            ),
            method="GET",
            headers=self.headers
        )
        domain_key = "d:{}".format(self.domain_model.id)
        site_key = "s:{}".format(self.site_model.id)
        r_data = json.loads(response.data)
        self.assertEquals(sorted(r_data["roles_map"][domain_key]),
                          sorted([self.role_model_1.id]))
        self.assertEquals(sorted(r_data["roles_map"][site_key]),
                          sorted([self.role_model_1.id, self.role_model_2.id])
        )

    def test_invitation_redeem_expired(self):
        """Test Case for when an invitation to be redeemed has expired.
        """
        response = self.client.open(
            "/api/v1/invitations/{invitation_id}/redeem/{user_id}".format(
                invitation_id=self.expired_invite.id, user_id="%s" % uuid.uuid1()
            ),
            method="GET",
            headers=self.headers
        )
        self.assertStatus(response, 410)
