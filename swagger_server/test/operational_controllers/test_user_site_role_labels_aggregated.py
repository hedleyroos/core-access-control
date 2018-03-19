# coding: utf-8

from __future__ import absolute_import
import random
import uuid

from access_control import db_actions
from flask import json
from six import BytesIO

from access_control.settings import API_KEY_HEADER
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
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": "%s" % uuid.uuid1(),
            "is_active": True,
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=site_data,
            action="create"
        )
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

        self.user_id = "%s" % uuid.uuid1()
        for role in self.roles:
            site_role_data = {
                "role_id": role.id,
                "site_id": self.site_model.id,
            }
            site_role_model = db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data=site_role_data,
                action="create"
            )

            user_site_role_data = {
                "role_id": role.id,
                "site_id": self.site_model.id,
                "user_id": self.user_id,
            }
            user_site_role_model = db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                data=user_site_role_data,
                action="create"
            )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_get_user_site_role_labels_aggregated(self):
        """Test case for get_user_site_role_labels_aggregated
        """
        response = self.client.open(
            "/api/v1/ops/user_site_role_labels_aggregated/{user_id}/{site_id}".format(
                user_id=self.user_id, site_id=self.site_model.id
        ),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data["roles"]), len(self.roles))
        for role in self.roles:
            self.assertIn(role.label, r_data["roles"])
        self.assertEqual(self.site_model.id, r_data["site_id"])
        self.assertEqual(self.user_id, r_data["user_id"])


if __name__ == '__main__':
    import unittest
    unittest.main()
