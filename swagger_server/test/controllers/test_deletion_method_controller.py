# coding: utf-8

from __future__ import absolute_import
import random
import uuid

import werkzeug
from flask import json
from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.models import DeletionMethod, DeletionMethodCreate, DeletionMethodUpdate  # noqa: E501
from swagger_server.test import BaseTestCase, db_create_entry


class DeletionMethodTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.headers = {API_KEY_HEADER: "test-api-key"}

    def test_deletion_method_create(self):
        data = DeletionMethodCreate(**{
            "label": ("%s" % uuid.uuid1())[:30],
            "data_schema": {"type": "object"},
            "description": "created something or other method",
        })
        response = self.client.open(
            '/api/v1/deletionmethods',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        for key, val in data.to_dict().items():
            self.assertEqual(r_data[key], val)

    def test_deletion_method_read(self):
        deletionmethod_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "data_schema": {"type": "object"},
            "description": "a super cool test method",
        }
        model = db_create_entry(
            model="DeletionMethod",
            data=deletionmethod_data,
        )
        response = self.client.open(
            '/api/v1/deletionmethods/{id}'.format(id=model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["label"], model.label)
        self.assertEqual(r_data["data_schema"], model.data_schema)
        self.assertEqual(r_data["description"], model.description)

    def test_deletion_method_delete(self):
        deletionmethod_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "data_schema": {"type": "object"},
            "description": "a super cool test method",
        }
        model = db_create_entry(
            model="DeletionMethod",
            data=deletionmethod_data,
        )
        response = self.client.open(
            '/api/v1/deletionmethods/{id}'.format(id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="DeletionMethod",
                api_model=DeletionMethod,
                action="read",
                query={"id": model.id}
            )

    def test_deletion_method_list(self):
        objects = []
        for index in range(1, random.randint(5, 20)):
            deletionmethod_data = {
                "label": ("%s" % uuid.uuid1())[:30],
                "data_schema": {"type": "object"},
                "description": "a super cool test method %s" % index,
            }
            objects.append(db_create_entry(
                model="DeletionMethod",
                data=deletionmethod_data,
            ))
        ids =  ",".join(map(str, [model.id for model in objects]))
        query_string = [('deletionmethod_ids', ids)]
        response = self.client.open(
            '/api/v1/deletionmethods',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects)+1)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects)+1)
        query_string = [
            ('limit', 2),
            ('deletionmethod_ids', ids)
        ]
        response = self.client.open(
            '/api/v1/deletionmethods',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects)+1)

    def test_role_update(self):
        data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "data_schema": {"type": "object"},
            "description": "a super cool test method",
        }
        model = db_create_entry(
            model="DeletionMethod",
            data=data,
        )
        data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "meh updated",
        }
        data = DeletionMethodUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/deletionmethods/{id}'.format(id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="DeletionMethod",
            api_model=DeletionMethod,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["label"], updated_entry.label)
        self.assertEqual(r_data["description"], updated_entry.description)
