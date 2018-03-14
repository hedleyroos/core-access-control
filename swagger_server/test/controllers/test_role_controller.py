# coding: utf-8

from __future__ import absolute_import

import random
import uuid

import os
import werkzeug

from flask import json

from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.role_update import RoleUpdate  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import db_actions


class TestAccessControlRead(BaseTestCase):

    def setUp(self):
        self.role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test role",
            "requires_2fa": True,
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )

        # Test env settings
        os.environ["ALLOWED_API_KEYS"] = "ahjaeK1thee9aixuogho"

        self.headers = {"X-API-KEY": "ahjaeK1thee9aixuogho"}

    def test_role_create(self):
        """Test case for role_create
        """
        data = Role(**{
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role to create",
            "requires_2fa": True,
        })
        response = self.client.open(
            '/api/v1/roles',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["label"], data.label)
        self.assertEqual(r_data["description"], data.description)

    def test_role_read(self):
        """Test case for role_read
        """
        response = self.client.open(
            '/api/v1/roles/{role_id}'.format(role_id=self.role_model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["label"], self.role_model.label)
        self.assertEqual(r_data["description"], self.role_model.description)
        self.assertEqual(r_data["id"], self.role_model.id)

    def test_role_delete(self):
        """Test case for role_delete
        """
        data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role to delete",
            "requires_2fa": True,
        }
        model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/roles/{role_id}'.format(role_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Role",
                api_model=Role,
                action="read",
                query={"id": model.id}
            )

    def test_role_list(self):
        """Test case for role_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "role list %s" % index,
                "requires_2fa": True,
            }
            objects.append(db_actions.crud(
                model="Role",
                api_model=Role,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('role_ids', ",".join(map(str, [role.id for role in objects])))]
        response = self.client.open(
            '/api/v1/roles',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [('limit', 2),
                        ('role_ids', ",".join(map(str, [role.id for role in objects])))]
        response = self.client.open(
            '/api/v1/roles',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_role_update(self):
        """Test case for role_update
        """
        data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role to update",
        }
        model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=data,
            action="create"
        )
        data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role updated",
        }
        data = RoleUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/roles/{role_id}'.format(role_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Role",
            api_model=Role,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["label"], updated_entry.label)
        self.assertEqual(r_data["description"], updated_entry.description)
