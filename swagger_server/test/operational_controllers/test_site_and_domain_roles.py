# coding: utf-8

from __future__ import absolute_import
import random
import uuid
from collections import OrderedDict

from ge_core_shared import db_actions, decorators
from flask import json

from project.settings import API_KEY_HEADER
from swagger_server.models.site_role import SiteRole  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.domain_role import DomainRole  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOperationalController(BaseTestCase):

    @decorators._db_exception
    def setUp(self):
        super().setUp()
        # Create top level parent domain.
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
        domain_role_data = {
            "role_id": role_model.id,
            "domain_id": self.domain_model.id
        }
        db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=domain_role_data,
            action="create"
        )

        # Set a single role on the top level domain.
        self.data = OrderedDict()
        self.data["d:%s" % self.domain_model.id] = [role_model.id]

        domain_id = self.domain_model.id
        for index in range(1, random.randint(5, 20)):
            # Create a domain tree with roles per domain.
            domain_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "%s" % uuid.uuid1(),
                "parent_id": domain_id
            }
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data=domain_data,
                action="create"
            )

            # Set id for next iteration.
            domain_id = domain_model.id
            roles = []

            self.data["d:%s" % domain_model.id] = []
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
                roles.append(role_model)
            for role in roles:
                domain_role_data = {
                    "role_id": role.id,
                    "domain_id": domain_model.id
                }
                db_actions.crud(
                    model="DomainRole",
                    api_model=DomainRole,
                    data=domain_role_data,
                    action="create"
                )
                self.data["d:%s" % domain_model.id].append(role.id)

        # Assign the site to the last domain in the tree.
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": domain_id,
            "description": "a super cool test site",
            "client_id": 0,
            "is_active": True,
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=site_data,
            action="create"
        )

        # create a bunch of roles for a site..
        self.data["s:%s" % self.site_model.id] = []
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
            site_role_data = {
                "role_id": role_model.id,
                "site_id": self.site_model.id,
            }
            site_role_model = db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data=site_role_data,
                action="create"
            )
            self.data["s:%s" % self.site_model.id].append(role_model.id)

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_get_site_and_domain_roles(self):
        """Test case for get_user_site_role_labels_aggregated
        """
        response = self.client.open(
            '/api/v1/ops/site_and_domain_roles/{site_id}'.format(site_id=self.site_model.id),
            method='GET', headers=self.headers)

        r_data = json.loads(response.data)
        roles = []

        # Each sub domain and finally the site also has the previous roles in
        # the tree as well as their own.
        for key, value in self.data.items():
            roles.extend(value)

            self.assertListEqual(sorted(r_data["roles_map"][key]), sorted(roles))


if __name__ == '__main__':
    import unittest
    unittest.main()
