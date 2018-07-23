# coding: utf-8

from __future__ import absolute_import
import random
import uuid

import werkzeug
from flask import json

from access_control import models
from project.settings import API_KEY_HEADER
from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server.models.resource_update import ResourceUpdate  # noqa: E501
from swagger_server.test import BaseTestCase
from ge_core_shared import db_actions


class ResourceTestCase(BaseTestCase):

    def setUp(self):
        self.resource_data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test resource",
        }
        self.resource_model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=self.resource_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def tearDown(self):
        models.RoleResourcePermission.query.delete()
        models.Resource.query.delete()

    def test_resource_create(self):
        """Test case for resource_create
        """
        data = Resource(**{
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "resource to create",
        })
        response = self.client.open(
            '/api/v1/resources',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["urn"], data.urn)
        self.assertEqual(r_data["description"], data.description)

    def test_resource_read(self):
        """Test case for resource_read
        """
        response = self.client.open(
            '/api/v1/resources/{resource_id}'.format(resource_id=self.resource_model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["urn"], self.resource_model.urn)
        self.assertEqual(r_data["description"], self.resource_model.description)
        self.assertEqual(r_data["id"], self.resource_model.id)

    def test_resource_delete(self):
        """Test case for resource_delete
        """
        data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "resource to delete",
        }
        model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/resources/{resource_id}'.format(resource_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Resource",
                api_model=Resource,
                action="read",
                query={"id": model.id}
            )

    def test_resource_list(self):
        """Test case for resource_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "urn": ("%s" % uuid.uuid1())[:30],
                "description": "resource list %s" % index,
            }
            objects.append(db_actions.crud(
                model="Resource",
                api_model=Resource,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('resource_ids', ",".join(map(str, [resource.id for resource in objects])))]
        response = self.client.open(
            '/api/v1/resources',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        query_string = [('limit', 2),
                        ('resource_ids', ",".join(map(str, [resource.id for resource in objects])))]
        response = self.client.open(
            '/api/v1/resources',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        # Test Prefix filter
        data = {
            "urn": ("custom:%s" % uuid.uuid1())[:24],
            "description": "custom resource",
        }
        db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=data,
            action="create"
        )
        query_string = [('prefix', "custom:")]
        response = self.client.open(
            '/api/v1/resources',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 1)
        self.assertEqual(int(response.headers["X-Total-Count"]), 1)

    def test_resource_update(self):
        """Test case for resource_update
        """
        data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "resource to update",
        }
        model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=data,
            action="create"
        )
        data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "resource updated",
        }
        data = ResourceUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/resources/{resource_id}'.format(resource_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Resource",
            api_model=Resource,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["urn"], updated_entry.urn)
        self.assertEqual(r_data["description"], updated_entry.description)
