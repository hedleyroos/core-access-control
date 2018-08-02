import random
import uuid

import werkzeug

from flask import json
from ge_core_shared import db_actions
from project.settings import API_KEY_HEADER
from unittest import mock

from swagger_server.models import Domain
from swagger_server.models import DomainRole
from swagger_server.models import Role
from swagger_server.models import UserDomainRole
from swagger_server.models import UserDomainRoleCreate
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.domain_create import DomainCreate
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.site_role import SiteRole  # noqa: E501
from swagger_server.models.user_deletion_data import UserDeletionData
from swagger_server.models.user_site_role import UserSiteRole  # noqa: E501
from swagger_server.models.user_site_role_create import UserSiteRoleCreate  # noqa: E501
from swagger_server.test import BaseTestCase


class DeleteUserDataTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.headers = {API_KEY_HEADER: "test-api-key"}

    def test_delete_user_data_usersiterole(self):
        user_id = "%s" % uuid.uuid1()
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data={
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data={
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        for index in range(1, 30):
            site_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "domain_id": domain_model.id,
                "description": "a super cool test site",
                "client_id": uuid.uuid1().int>>97,
                "is_active": True,
            }
            site_model = db_actions.crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
            db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                },
                action="create"
            )
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                    "user_id": user_id,
                },
                action="create"
            )

        response = self.client.open(
            '/api/v1/ops/users/{user_id}/delete'.format(
                user_id=user_id,
            ), method='GET',
            headers=self.headers)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["amount"], 29)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                action="read",
                query={
                    "user_id": user_id,
                }
            )

    def test_delete_user_data_userdomainrole(self):
        user_id = "%s" % uuid.uuid1()
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data={
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        for index in range(1, 35):
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data={
                    "name": ("%s" % uuid.uuid1())[:30],
                    "description": "user_site_role to create",
                },
                action="create"
            )
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id
                },
                action="create"
            )
            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id,
                    "user_id": user_id
                },
                action="create"
            )

        response = self.client.open(
            '/api/v1/ops/users/{user_id}/delete'.format(
                user_id=user_id,
            ), method='GET',
            headers=self.headers)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["amount"], 34)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                action="read",
                query={
                    "user_id": user_id,
                }
            )

    def test_delete_user_data_combined(self):
        user_id = "%s" % uuid.uuid1()
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data={
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data={
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        for index in range(1, 30):
            site_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "domain_id": domain_model.id,
                "description": "a super cool test site",
                "client_id": uuid.uuid1().int>>97,
                "is_active": True,
            }
            site_model = db_actions.crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
            db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                },
                action="create"
            )
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                    "user_id": user_id,
                },
                action="create"
            )
        for index in range(1, 35):
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data={
                    "name": ("%s" % uuid.uuid1())[:30],
                    "description": "user_site_role to create",
                },
                action="create"
            )
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id
                },
                action="create"
            )
            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id,
                    "user_id": user_id
                },
                action="create"
            )

        response = self.client.open(
            '/api/v1/ops/users/{user_id}/delete'.format(
                user_id=user_id,
            ), method='GET',
            headers=self.headers)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["amount"], 63)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                action="read",
                query={
                    "user_id": user_id,
                }
            )

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                action="read",
                query={
                    "user_id": user_id,
                }
            )

    def test_sql_atomic_nature(self):
        user_id = "%s" % uuid.uuid1()
        role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data={
                "label": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data={
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            },
            action="create"
        )
        for index in range(1, 30):
            site_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "domain_id": domain_model.id,
                "description": "a super cool test site",
                "client_id": uuid.uuid1().int>>97,
                "is_active": True,
            }
            site_model = db_actions.crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
            db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                },
                action="create"
            )
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                data={
                    "role_id": role_model.id,
                    "site_id": site_model.id,
                    "user_id": user_id,
                },
                action="create"
            )
        for index in range(1, 35):
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data={
                    "name": ("%s" % uuid.uuid1())[:30],
                    "description": "user_site_role to create",
                },
                action="create"
            )
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id
                },
                action="create"
            )
            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                data={
                    "role_id": role_model.id,
                    "domain_id": domain_model.id,
                    "user_id": user_id
                },
                action="create"
            )

        # SQL being mocked needs to break, to ensure nothing is committed
        # unless the entire query is successful
        mocked_sql = """
        -- Given a user id (:user_id),
        -- delete UserDomainRoles and UserSiteRoles tied to user id

        WITH deleted_site_roles AS (
            DELETE FROM user_site_role
                WHERE user_id = :user_id
            RETURNING user_id
        ),
        deleted_domain_roles AS (
            DELETE FROM fooooooo -- This is meant to break
                WHERE none_valid = :user_id
            RETURNING user_id
        ),
        deleted_rows AS (
           SELECT * FROM deleted_site_roles
           UNION ALL  -- ALL is required so that duplicates are not dropped
           SELECT * FROM deleted_domain_roles
        )

        SELECT COUNT(*) AS amount
          FROM deleted_rows;
        """
        with mock.patch(
                "swagger_server.controllers.operational_controller.SQL_DELETE_USER_DATA",
                new_callable=lambda: mocked_sql):
            response = self.client.open(
                '/api/v1/ops/users/{user_id}/delete'.format(
                    user_id=user_id,
                ), method='GET',
                headers=self.headers)

        response_data = json.loads(response.data)
        self.assertIn(
            'relation "fooooooo" does not e',
            response_data["error"]
        )
        site_roles = db_actions.crud(
            model="UserSiteRole",
            api_model=UserSiteRole,
            action="list",
            query={
                "order_by": ["user_id"],
                "ids": {
                    "user_id": user_id
                }
            }
        )
        self.assertEqual(len(site_roles[0]), 29)
        domain_roles = db_actions.crud(
            model="UserDomainRole",
            api_model=UserDomainRole,
            action="list",
            query={
                "order_by": ["user_id"],
                "ids": {
                    "user_id": user_id
                }
            }
        )
        self.assertEqual(len(domain_roles[0]), 34)
