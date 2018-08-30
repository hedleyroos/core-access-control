# coding: utf-8

from __future__ import absolute_import

from ge_core_shared import db_actions, decorators
from flask import json

from project.settings import API_KEY_HEADER
from swagger_server.models import Permission, Resource, Role, RoleResourcePermission
from swagger_server.test import BaseTestCase


class TestOperationalController(BaseTestCase):
    NUM_TESTS = 10

    @decorators.db_exception
    def setUp(self):
        super().setUp()
        self.headers = {API_KEY_HEADER: "test-api-key"}
        self.role_ids = []

        for i in range(0, self.NUM_TESTS):
            # Create permission
            data = {
                "name": f"permission_{i}",
                "description": f"Permission {i}",
            }
            permission = db_actions.crud(
                model="Permission",
                api_model=Permission,
                data=data,
                action="create"
            )

            # Create resource
            data = {
                "urn": f"resource_{i}",
                "description": f"Resource {i}",
            }
            resource = db_actions.crud(
                model="Resource",
                api_model=Resource,
                data=data,
                action="create"
            )

            # Create role
            data = {
                "label": f"role_{i}",
                "description": f"Role {i}",
            }
            role = db_actions.crud(
                model="Role",
                api_model=Role,
                data=data,
                action="create"
            )
            self.role_ids.append(role.id)

            # Create role resource permission
            data = {
                "role_id": role.id,
                "resource_id": resource.id,
                "permission_id": permission.id
            }
            role_resource_permission = db_actions.crud(
                model="RoleResourcePermission",
                api_model=RoleResourcePermission,
                data=data,
                action="create"
            )

    def test_get_resource_permissions_for_roles(self):
        """Test case for get_user_site_role_labels_aggregated
        """
        for i in range(1, 10):
            response = self.client.open(
                '/api/v1/ops/resource_permissions_for_roles?role_ids={}'.format(
                    ",".join(str(e) for e in self.role_ids[0:i])),
                method='GET', headers=self.headers)

            r_data = json.loads(response.data)
            self.assertEqual(len(r_data), i)

        # Specifying no role_ids returns an HTTP 400
        response = self.client.open(
            '/api/v1/ops/resource_permissions_for_roles?role_ids=',
            method='GET', headers=self.headers)

        self.assertEqual(response.status_code, 400)
