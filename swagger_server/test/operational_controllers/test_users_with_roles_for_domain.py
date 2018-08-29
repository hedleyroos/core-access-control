import json
import uuid

from ge_core_shared import db_actions, decorators

from project.settings import API_KEY_HEADER
from swagger_server.test import BaseTestCase
from swagger_server.models.domain import Domain
from swagger_server.models.domain_role import DomainRole
from swagger_server.models.role import Role
from swagger_server.models.user_domain_role import UserDomainRole

ROLES = [
    {
        "label": ("%s" % uuid.uuid1())[:30],
        "description": "Role to view"
    },
    {
        "label": ("%s" % uuid.uuid1())[:30],
        "description": "Role to create",
    },
    {
        "label": ("%s" % uuid.uuid1())[:30],
        "description": "Role to delete",
    }
]


class TestUsersWithRolesForDomain(BaseTestCase):

    @decorators._db_exception
    def setUp(self):
        super().setUp()
        # Parent Domain
        self.domain_parent_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "The Root Domain",
        }
        self.domain_parent_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_parent_data,
            action="create"
        )
        # Child Domain
        self.domain_child_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "The Child Domain",
            "parent_id": self.domain_parent_model.id
        }
        self.domain_child_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_child_data,
            action="create"
        )
        # Create some roles.
        self.roles = []
        for role in ROLES:
            role_model = db_actions.crud(
                model="Role",
                api_model=Role,
                data=role,
                action="create"
            )
            self.roles.append(role_model)
        # Some users as well.
        self.user_id_1 = "%s" % uuid.uuid1()
        self.user_id_2 = "%s" % uuid.uuid1()

        for role in self.roles:
            domain_role_data = {
                "domain_id": self.domain_parent_model.id,
                "role_id": role.id,
                "grant_implicitly": "view" in role.description
            }
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data=domain_role_data,
                action="create"
            )
            if not domain_role_data["grant_implicitly"]:
                user_domain_role_data = {
                    "user_id": self.user_id_1,
                    "domain_id": self.domain_parent_model.id,
                    "role_id": role.id
                }
                db_actions.crud(
                    model="UserDomainRole",
                    api_model=UserDomainRole,
                    data=user_domain_role_data,
                    action="create"
                )
            domain_role_data = {
                "domain_id": self.domain_child_model.id,
                "role_id": role.id,
                "grant_implicitly": "view" in role.description
            }
            db_actions.crud(
                model="DomainRole",
                api_model=DomainRole,
                data=domain_role_data,
                action="create"
            )
            if "create" in role.description:
                user_domain_role_data = {
                    "user_id": self.user_id_2,
                    "domain_id": self.domain_child_model.id,
                    "role_id": role.id
                }
                db_actions.crud(
                    model="UserDomainRole",
                    api_model=UserDomainRole,
                    data=user_domain_role_data,
                    action="create"
                )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_get_users_with_roles_for_domain(self):
        """Test case for get_users_with_roles_for_domain
        """
        response = self.client.open(
            "/api/v1/ops/users_with_roles_for_domain/{domain_id}".format(
                domain_id=self.domain_child_model.id
            ), method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEquals(len(r_data), 2)
        for user in r_data:
            self.assertEquals(
                len(user["role_ids"]),
                2 if user["user_id"] == self.user_id_1 else 1
            )


if __name__ == '__main__':
    import unittest
    unittest.main()
