# coding: utf-8

from __future__ import absolute_import
import random
import uuid

import werkzeug
from flask import json

from access_control.settings import API_KEY_HEADER
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.site_update import SiteUpdate  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.test import BaseTestCase
from access_control import db_actions


class TestAccessControlRead(BaseTestCase):

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
        self.site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": uuid.uuid1().int>>97,
            "is_active": True,
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_site_create(self):
        """Test case for site_create
        """
        data = Site(**{
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": "%s" % (uuid.uuid1().int>>97),
            "is_active": True,
        })
        response = self.client.open(
            '/api/v1/sites',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], data.name)
        self.assertEqual(r_data["domain_id"], data.domain_id)
        self.assertEqual(r_data["description"], data.description)
        self.assertEqual(r_data["client_id"], data.client_id)
        self.assertEqual(r_data["is_active"], data.is_active)

    def test_site_read(self):
        """Test case for site_read
        """
        response = self.client.open(
            '/api/v1/sites/{site_id}'.format(site_id=self.site_model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], self.site_model.name)
        self.assertEqual(r_data["domain_id"], self.site_model.domain_id)
        self.assertEqual(r_data["client_id"], self.site_model.client_id)
        self.assertEqual(r_data["description"], self.site_model.description)
        self.assertEqual(r_data["id"], self.site_model.id)
        self.assertEqual(r_data["is_active"], self.site_model.is_active)

    def test_site_delete(self):
        """Test case for site_delete
        """
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": uuid.uuid1().int>>97,
            "is_active": True,
        }
        model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/sites/{site_id}'.format(site_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Site",
                api_model=Site,
                action="read",
                query={"id": model.id}
            )

    def test_site_list(self):
        """Test case for site_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "domain_id": self.domain_model.id,
                "description": "a super cool test site",
                "client_id": uuid.uuid1().int>>97,
                "is_active": True,
            }
            objects.append(db_actions.crud(
                model="Site",
                api_model=Site,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('site_ids', ",".join(map(str, [site.id for site in objects])))]
        response = self.client.open(
            '/api/v1/sites',
            method='GET',
            query_string=query_string, headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [('limit', 2),
                        ('site_ids', ",".join(map(str, [site.id for site in objects])))]
        response = self.client.open(
            '/api/v1/sites',
            method='GET',
            query_string=query_string, headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_site_update(self):
        """Test case for site_update
        """
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": uuid.uuid1().int>>97,
            "is_active": True,
        }
        model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=data,
            action="create"
        )
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "site updated",
            "client_id": "%s" % (uuid.uuid1().int>>97),
            "is_active": False,
        }
        data = SiteUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/sites/{site_id}'.format(site_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Site",
            api_model=Site,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["name"], updated_entry.name)
        self.assertEqual(r_data["description"], updated_entry.description)
        self.assertEqual(r_data["client_id"], updated_entry.client_id)
        self.assertEqual(r_data["is_active"], updated_entry.is_active)
