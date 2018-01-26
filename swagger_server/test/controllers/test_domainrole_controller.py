# coding: utf-8

from __future__ import absolute_import

import datetime
import random
import uuid
import werkzeug

from flask import json
from six import BytesIO

from swagger_server.models.domain_role import DomainRole  # noqa: E501
from swagger_server.models.domain_role_create import DomainRoleCreate  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.permission import Permission  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import models, db_actions


class TestAccessControlRead(BaseTestCase):

    def setUp(self):
        self.role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )
        self.domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "domain to create",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_data,
            action="create"
        )

        self.domain_role_data = {
            "role_id": self.role_model.id,
            "domain_id": self.domain_model.id,
        }
        self.domain_role_model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=self.domain_role_data,
            action="create"
        )

    def test_domain_role_create(self):
        """Test case for domain_role_create
        """
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )

        data = DomainRoleCreate(**{
            "role_id": role_model.id,
            "domain_id": domain_model.id,
            "grant_implicitly": True,
        })
        response = self.client.open(
            '/api/v1/domainroles/',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["domain_id"], data.domain_id)

    def test_domain_role_read(self):
        """Test case for domain_role_read
        """
        response = self.client.open(
            '/api/v1/domainroles/{domain_id}/{role_id}/'.format(
                domain_id=self.domain_role_model.domain_id,
                role_id=self.domain_role_model.role_id,
            ),
            method='GET')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], self.domain_role_model.role_id)
        self.assertEqual(r_data["domain_id"], self.domain_role_model.domain_id)

    def test_domain_role_delete(self):
        """Test case for domain_role_delete
        """
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )

        domain_role_data = {
            "role_id": role_model.id,
            "domain_id": domain_model.id,
        }
        model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=domain_role_data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/domainroles/{domain_id}/{role_id}/'.format(
                domain_id=model.domain_id,
                role_id=model.role_id,
            ),
            method='DELETE')

        # Little crude. Raise an error if the object actually still exists else
        # pass after the 404 error.
        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                action="read",
                query={
                    "role_id": model.role_id,
                    "domain_id": model.domain_id,
                }
            )

    def test_domain_role_list(self):
        """Test case for domain_role_list
        """
        objects = []
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        for index in range(3, random.randint(4, 20)):
            domain_data = {
                "name": ("%s" % uuid.uuid4())[:30],
                "description": "domain_role to create",
            }
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data=domain_data,
                action="create"
            )

            domain_role_data = {
                "role_id": role_model.id,
                "domain_id": domain_model.id,
            }
            objects.append(db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data=domain_role_data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/domainroles/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [#('offset', 0),
                        ('limit', 2),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/domainroles/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_domain_role_update(self):
        """Test case for domain_role_update
        """
        role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
        domain_role_data = {
            "role_id": role_model.id,
            "domain_id": domain_model.id,
        }
        domain_role_model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=domain_role_data,
            action="create"
        )

        # Change domain on the model.
        domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "domain_role to create",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
        data = {
            "role_id": role_model.id,
            "domain_id": domain_model.id,
        }
        data = DomainRoleCreate(
            **data
        )
        response = self.client.open(
            '/api/v1/domainroles/{domain_id}/{role_id}/'.format(
                domain_id=domain_role_model.domain_id,
                role_id=domain_role_model.role_id,
            ),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            action="read",
            query={
                "role_id": data.role_id,
                "domain_id": data.domain_id,
            }
        )
        self.assertEqual(r_data["role_id"], updated_entry.role_id)
        self.assertEqual(r_data["domain_id"], updated_entry.domain_id)
