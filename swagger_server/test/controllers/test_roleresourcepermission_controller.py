# coding: utf-8

from __future__ import absolute_import
import random
import uuid

import werkzeug
from flask import json

from project.settings import API_KEY_HEADER
from swagger_server.models.role_resource_permission import RoleResourcePermission  # noqa: E501
from swagger_server.models.role_resource_permission_create import RoleResourcePermissionCreate  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server.models.permission import Permission  # noqa: E501
from swagger_server.test import BaseTestCase
from ge_core_shared import db_actions


class RoleResourcePermissionTestCase(BaseTestCase):

    def setUp(self):
        self.role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )
        self.resource_data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        self.resource_model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=self.resource_data,
            action="create"
        )
        self.permission_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        self.permission_model = db_actions.crud(
            model="Permission",
            api_model=Permission,
            data=self.permission_data,
            action="create"
        )

        self.role_resource_permission_data = {
            "role_id": self.role_model.id,
            "resource_id": self.resource_model.id,
            "permission_id": self.permission_model.id,
        }
        self.role_resource_permission_model = db_actions.crud(
            model="RoleResourcePermission",
            api_model=RoleResourcePermission,
            data=self.role_resource_permission_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_role_resource_permission_create(self):
        """Test case for role_resource_permission_create
        """
        role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        resource_data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        resource_model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=resource_data,
            action="create"
        )
        permission_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        permission_model = db_actions.crud(
            model="Permission",
            api_model=Permission,
            data=permission_data,
            action="create"
        )

        data = RoleResourcePermissionCreate(**{
            "role_id": self.role_model.id,
            "resource_id": resource_model.id,
            "permission_id": permission_model.id,
        })
        response = self.client.open(
            '/api/v1/roleresourcepermissions',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["resource_id"], data.resource_id)
        self.assertEqual(r_data["permission_id"], data.permission_id)

    def test_role_resource_permission_read(self):
        """Test case for role_resource_permission_read
        """
        response = self.client.open(
            '/api/v1/roleresourcepermissions/{role_id}/{resource_id}/{permission_id}'.format(
                role_id=self.role_resource_permission_model.role_id,
                resource_id=self.role_resource_permission_model.resource_id,
                permission_id=self.role_resource_permission_model.permission_id,
            ),
            method='GET',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], self.role_resource_permission_model.role_id)
        self.assertEqual(r_data["resource_id"], self.role_resource_permission_model.resource_id)
        self.assertEqual(r_data["permission_id"], self.role_resource_permission_model.permission_id)

    def test_role_resource_permission_delete(self):
        """Test case for role_resource_permission_delete
        """
        role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        resource_data = {
            "urn": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        resource_model = db_actions.crud(
            model="Resource",
            api_model=Resource,
            data=resource_data,
            action="create"
        )
        permission_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        permission_model = db_actions.crud(
            model="Permission",
            api_model=Permission,
            data=permission_data,
            action="create"
        )

        role_resource_permission_data = {
            "role_id": role_model.id,
            "resource_id": resource_model.id,
            "permission_id": permission_model.id,
        }
        model = db_actions.crud(
            model="RoleResourcePermission",
            api_model=RoleResourcePermission,
            data=role_resource_permission_data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/roleresourcepermissions/{role_id}/{resource_id}/{permission_id}'.format(
                role_id=model.role_id,
                resource_id=model.resource_id,
                permission_id=model.permission_id,
            ),
            method='DELETE',
            headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="RoleResourcePermission",
                api_model=RoleResourcePermission,
                action="read",
                query={
                    "role_id": model.role_id,
                    "resource_id": model.resource_id,
                    "permission_id": model.permission_id,
                }
            )

    def test_role_resource_permission_list(self):
        """Test case for role_resource_permission_list
        """
        objects = []
        role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "role_resource_permission to create",
        }
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=role_data,
            action="create"
        )
        for index in range(1, random.randint(5, 20)):
            resource_data = {
                "urn": ("%s" % uuid.uuid1())[:30],
                "description": "role_resource_permission to create",
            }
            resource_model = db_actions.crud(
                model="Resource",
                api_model=Resource,
                data=resource_data,
                action="create"
            )
            permission_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "role_resource_permission to create",
            }
            permission_model = db_actions.crud(
                model="Permission",
                api_model=Permission,
                data=permission_data,
                action="create"
            )

            role_resource_permission_data = {
                "role_id": role_model.id,
                "resource_id": resource_model.id,
                "permission_id": permission_model.id,
            }
            objects.append(db_actions.crud(
                model="RoleResourcePermission",
                api_model=RoleResourcePermission,
                data=role_resource_permission_data,
                action="create"
            ))
        print ("Role: %s" % role_model.id)
        query_string = [#('offset', 0),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/roleresourcepermissions',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        query_string = [#('offset', 0),
                        ('limit', 2),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/roleresourcepermissions',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))

    #def test_role_resource_permission_update(self):
    #    """Test case for role_resource_permission_update
    #    """
    #    data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission to update",
    #    }
    #    model = db_actions.crud(
    #        model="RoleResourcePermission",
    #        api_model=RoleResourcePermission,
    #        data=data,
    #        action="create"
    #    )
    #    data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission updated",
    #    }
    #    role_data = {
    #        "label": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission to create",
    #    }
    #    role_model = db_actions.crud(
    #        model="Role",
    #        api_model=Role,
    #        data=role_data,
    #        action="create"
    #    )
    #    resource_data = {
    #        "urn": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission to create",
    #    }
    #    resource_model = db_actions.crud(
    #        model="Resource",
    #        api_model=Resource,
    #        data=resource_data,
    #        action="create"
    #    )
    #    permission_data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission to create",
    #    }
    #    permission_model = db_actions.crud(
    #        model="Permission",
    #        api_model=Permission,
    #        data=permission_data,
    #        action="create"
    #    )
    #    role_resource_permission_data = {
    #        "role_id": role_model.id,
    #        "resource_id": resource_model.id,
    #        "permission_id": permission_model.id,
    #    }
    #    role_resource_permission_model = db_actions.crud(
    #        model="RoleResourcePermission",
    #        api_model=RoleResourcePermission,
    #        data=role_resource_permission_data,
    #        action="create"
    #    )

    #    # Change permission on the model.
    #    permission_data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "description": "role_resource_permission to create",
    #    }
    #    permission_model = db_actions.crud(
    #        model="Permission",
    #        api_model=Permission,
    #        data=permission_data,
    #        action="create"
    #    )
    #    data = {
    #        "role_id": role_model.id,
    #        "resource_id": resource_model.id,
    #        "permission_id": permission_model.id,
    #    }
    #    data = RoleResourcePermissionCreate(
    #        **data
    #    )
    #    response = self.client.open(
    #        '/api/v1/roleresourcepermissions/{role_id}/{resource_id}/{permission_id}'.format(
    #            role_id=self.role_resource_permission_model.role_id,
    #            resource_id=self.role_resource_permission_model.role_id,
    #            permission_id=self.role_resource_permission_model.role_id,
    #        ),
    #        method='PUT',
    #        data=json.dumps(data),
    #        content_type='application/json')
    #    r_data = json.loads(response.data)
    #    updated_entry = db_actions.crud(
    #        model="RoleResourcePermission",
    #        api_model=RoleResourcePermission,
    #        action="read",
    #        query={
    #            "role_id": data.role_id,
    #            "resource_id": data.resource_id,
    #            "permission_id": data.permission_id
    #        }
    #    )
    #    self.assertEqual(r_data["role_id"], updated_entry.role_id)
    #    self.assertEqual(r_data["resource_id"], updated_entry.resource_id)
    #    self.assertEqual(r_data["permission_id"], updated_entry.permission_id)
