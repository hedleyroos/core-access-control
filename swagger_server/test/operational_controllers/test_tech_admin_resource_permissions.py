# coding: utf-8

from __future__ import absolute_import
import random
import uuid

from ge_core_shared import db_actions
from flask import json

from access_control import models
from project.settings import API_KEY_HEADER
from swagger_server.models import Permission, Resource
from swagger_server.test import BaseTestCase


class TestOperationalController(BaseTestCase):
    NUM_PERMISSIONS = 5
    NUM_RESOURCES = 10

    def setUp(self):
        self.headers = {API_KEY_HEADER: "test-api-key"}
        # Clear tables
        models.RoleResourcePermission.query.delete()
        models.UserDomainRole.query.delete()
        models.UserSiteRole.query.delete()
        models.DomainRole.query.delete()
        models.SiteRole.query.delete()
        models.Role.query.delete()
        models.Resource.query.delete()
        models.Permission.query.delete()

        for i in range(0, self.NUM_PERMISSIONS):
            data = {
                "name": f"permission_{i}",
                "description": f"Permission {i}",
            }
            model = db_actions.crud(
                model="Permission",
                api_model=Permission,
                data=data,
                action="create"
            )

        for j in range(0, self.NUM_RESOURCES):
            data = {
                "urn": f"resource_{j}",
                "description": f"Resource {j}",
            }
            model = db_actions.crud(
                model="Resource",
                api_model=Resource,
                data=data,
                action="create"
            )

    def test_get_tech_admin_resource_permissions(self):
        """We expect the cross product between all resources and permissions
        to be returned. In total there should be NUM_RESOURCES * NUM_PERMISSIONS results.
        """
        response = self.client.open(
            '/api/v1/ops/tech_admin_resource_permissions',
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), self.NUM_RESOURCES * self.NUM_PERMISSIONS)
