# coding: utf-8

from __future__ import absolute_import
import random
import uuid

import os

from access_control import db_actions
from flask import json
from six import BytesIO

from swagger_server.models.all_user_roles import AllUserRoles  # noqa: E501
from swagger_server.models.domain_roles import DomainRoles  # noqa: E501
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles  # noqa: E501
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_site_role import UserSiteRole  # noqa: E501
from swagger_server.models.user_site_role_create import UserSiteRoleCreate  # noqa: E501
from swagger_server.models.site_role import SiteRole  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models import DomainRole
from swagger_server.models import UserDomainRoleCreate
from swagger_server.test import BaseTestCase


class TestOperationalController(BaseTestCase):

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
        self.headers = {"X-API-KEY": "test-api-key"}

        self.roles = []
        # create a bunch of roles.
        for index in range(1, random.randint(5, 20)):
            role_data = {
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            }
            role_model = db_actions.crud(
                model="Role",
                api_model=Role,
                data=role_data,
                action="create"
            )
            self.roles.append(role_model)

        # Set domain roles as well.
        self.domain_data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test domain",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_data,
            action="create"
        )

        self.domain_role_objs = []
        for role in self.roles:
            domain_role_data = {
                "role_id": role.id,
                "domain_id": self.domain_model.id
            }
            self.domain_role_objs.append(db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data=domain_role_data,
                action="create"
            ))

    def test_get_domain_roles(self):
        """Test case for get_user_site_role_labels_aggregated
        """
        response = self.client.open(
            '/api/v1/ops/domain_roles/{domain_id}'.format(domain_id=self.domain_model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertIn("d:%s" % self.domain_model.id, r_data["roles_map"].keys())
        self.assertEqual(len(r_data["roles_map"]["d:%s" % self.domain_model.id]), len(self.roles))
        for obj in self.domain_role_objs:
            self.assertIn(obj.role_id, r_data["roles_map"]["d:%s" % self.domain_model.id])
        self.assertEqual(self.domain_model.id, r_data["domain_id"])
