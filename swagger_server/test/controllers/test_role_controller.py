# coding: utf-8

from __future__ import absolute_import

import datetime
import random
import uuid
import werkzeug

from flask import json
from six import BytesIO

from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.role_update import RoleUpdate  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import models, db_actions


class TestAccessControlRead(BaseTestCase):

    def setUp(self):
        self.role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test role",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )

    def test_role_create(self):
        """Test case for role_create
        """
        data = Role(**{
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "role to create",
        })
        response = self.client.open(
            '/api/v1/roles/',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["label"], data.label)
        self.assertEqual(r_data["description"], data.description)

    def test_role_read(self):
        """Test case for role_read
        """
        response = self.client.open(
            '/api/v1/roles/{role_id}/'.format(role_id=self.role_model.id),
            method='GET')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["label"], self.role_model.label)
        self.assertEqual(r_data["description"], self.role_model.description)
        self.assertEqual(r_data["id"], self.role_model.id)

    def test_role_delete(self):
        """Test case for role_delete
        """
        data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "role to delete",
        }
        model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/roles/{role_id}/'.format(role_id=model.id),
            method='DELETE')

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
        for index in range(3, random.randint(4, 20)):
            data = {
                "label": ("%s" % uuid.uuid4())[:30],
                "description": "role list %s" % index,
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
            '/api/v1/roles/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [('limit', 2),
                        ('role_ids', ",".join(map(str, [role.id for role in objects])))]
        response = self.client.open(
            '/api/v1/roles/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_role_update(self):
        """Test case for role_update
        """
        data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "role to update",
        }
        model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=data,
            action="create"
        )
        data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "role updated",
        }
        data = RoleUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/roles/{role_id}/'.format(role_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Role",
            api_model=Role,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["label"], updated_entry.label)
        self.assertEqual(r_data["description"], updated_entry.description)
