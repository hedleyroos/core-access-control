import random
import werkzeug
from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.models import InvitationRedirectUrl, InvitationRedirectUrlCreate, \
    InvitationRedirectUrlUpdate
from swagger_server.test import BaseTestCase
from flask import json


class InvitationRedirectUrlTestCase(BaseTestCase):

    @decorators.db_exception
    def setUp(self):
        super().setUp()

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

    def test_invitationredirecturl_create(self):
        data = InvitationRedirectUrlCreate(**{
            "url": "http://example.com/redirect?foo=bar",
            "description": "A test URL",
        })
        response = self.client.open(
            '/api/v1/invitationredirecturls',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["url"], data.url)
        self.assertEqual(r_data["description"], data.description)
        self.assertIn("id", r_data)
        self.assertIn("created_at", r_data)
        self.assertIn("updated_at", r_data)

        # With bad URLs
        for bad_url in [
            "ftp://example.com/redirect?foo=bar",  # Invalid scheme
            "http:/example.com/redirect?foo=bar",  # Incorrect ://
            "thisisjustamess",                     # Totally bogus
        ]:
            data = InvitationRedirectUrlCreate(**{
                "url": bad_url,
                "description": "A test URL",
            })
            response = self.client.open(
                '/api/v1/invitationredirecturls',
                method='POST',
                data=json.dumps(data),
                content_type='application/json',
                headers=self.headers)
            self.assertEqual(response.status_code, 400)

    def test_invitationredirecturl_read(self):
        """Test case for invitationredirecturl_read
        """
        response = self.client.open(
            '/api/v1/invitationredirecturls/{invitationredirecturl_id}'.format(
                invitationredirecturl_id=self.invitation_redirect_url.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["id"], self.invitation_redirect_url.id)
        self.assertEqual(r_data["url"], self.invitation_redirect_url.url)
        self.assertEqual(r_data["description"], self.invitation_redirect_url.description)

    def test_invitationredirecturl_delete(self):
        """Test case for invitationredirecturl_delete
        """
        data = {
            "url": "http://example.com/another/test",
            "description": "The deletion test URL",
        }
        model = db_actions.crud(
            model="InvitationRedirectUrl",
            api_model=InvitationRedirectUrl,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/invitationredirecturls/{invitationredirecturl_id}'.format(
                invitationredirecturl_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="InvitationRedirectUrl",
                api_model=InvitationRedirectUrl,
                action="read",
                query={"id": model.id}
            )

    def test_invitationredirecturl_list(self):
        """Test case for invitationredirecturl_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "url": f"http://example.com/{index}",
                "description": f"Description {index}",
            }
            objects.append(db_actions.crud(
                model="InvitationRedirectUrl",
                api_model=InvitationRedirectUrl,
                data=data,
                action="create"
            ))
        query_string = [
            ('invitationredirecturl_ids', ",".join(
                map(str, [invitation.id for invitation in objects])))]
        response = self.client.open(
            '/api/v1/invitationredirecturls',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        query_string = [('limit', 2),
                        ('invitation_ids', ",".join(map(str, [invitation.id for invitation in objects])))]
        response = self.client.open(
            '/api/v1/invitationredirecturls',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]),
                         len(objects)+1)  # +1 to count instance created in setUp()

    def test_invitationredirecturl_update(self):
        """Test case for invitationredirecturl_update
        """
        data = {
            "url": "http://example.com/redirect/1",
            "description": "Description goes here",
        }
        model = db_actions.crud(
            model="InvitationRedirectUrl",
            api_model=InvitationRedirectUrl,
            data=data,
            action="create"
        )
        data = {
            "url": "http://example.com/redirect/2",
            "description": "Updated description goes here",
        }
        data = InvitationRedirectUrlUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/invitationredirecturls/{invitationredirecturl_id}'.format(
                invitationredirecturl_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="InvitationRedirectUrl",
            api_model=InvitationRedirectUrl,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["url"], updated_entry.url)
        self.assertEqual(r_data["description"], updated_entry.description)

        # Attempt to update with bad URL
        data = {
            "url": "bad url",
            "description": "Updated description goes here",
        }
        data = InvitationRedirectUrlUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/invitationredirecturls/{invitationredirecturl_id}'.format(
                invitationredirecturl_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        self.assertEqual(response.status_code, 400)
