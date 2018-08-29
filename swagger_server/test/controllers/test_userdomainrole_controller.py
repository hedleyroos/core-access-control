import random
import uuid

import werkzeug

from ge_core_shared import db_actions, decorators
from project.settings import API_KEY_HEADER
from swagger_server.models import Domain
from swagger_server.models import DomainRole
from swagger_server.models import Role
from swagger_server.models import UserDomainRole
from swagger_server.models import UserDomainRoleCreate
from swagger_server.test import BaseTestCase
from flask import json


class UserDomainRoleTestCase(BaseTestCase):

    @decorators._db_exception
    def setUp(self):
        super().setUp()
        self.role_data = {
            "label": ("%s" % uuid.uuid4())[:30],
            "description": "user_site_role to create",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )
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

        self.domain_role_data = {
            "role_id": self.role_model.id,
            "domain_id": self.domain_model.id
        }
        self.domain_role_model = db_actions.crud(
            model="DomainRole",
            api_model=DomainRole,
            data=self.domain_role_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_userdomainrole_create(self):
        data = UserDomainRoleCreate(**{
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "user_id": "%s" % uuid.uuid1()
        })
        response = self.client.open(
            '/api/v1/userdomainroles',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["domain_id"], data.domain_id)

    def test_userdomainrole_delete(self):
        data = {
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "user_id": "%s" % uuid.uuid1()
        }
        user_domain_role = db_actions.crud(
            model="UserDomainRole",
            api_model=UserDomainRole,
            data=data,
            action="create"
        )

        with self.assertRaises(werkzeug.exceptions.NotFound):
            response = self.client.open(
                '/api/v1/userdomainroles/{user_id}/{domain_id}/{role_id}'.format(
                    user_id=user_domain_role.user_id,
                    domain_id=user_domain_role.domain_id,
                    role_id=user_domain_role.role_id,
                ),
                method='DELETE',
                headers=self.headers)

            db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                action="read",
                query={
                    "role_id": user_domain_role.role_id,
                    "domain_id": user_domain_role.domain_id,
                }
            )

    def test_userdomainrole_read(self):
        data = {
            "domain_id": self.domain_model.id,
            "role_id": self.role_model.id,
            "user_id": "%s" % uuid.uuid1()
        }
        user_domain_role = db_actions.crud(
            model="UserDomainRole",
            api_model=UserDomainRole,
            data=data,
            action="create"
        )

        response = self.client.open(
            '/api/v1/userdomainroles/{user_id}/{domain_id}/{role_id}'.format(
                user_id=user_domain_role.user_id,
                domain_id=user_domain_role.domain_id,
                role_id=user_domain_role.role_id,
            ),
            method='GET',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], user_domain_role.role_id)
        self.assertEqual(r_data["domain_id"], user_domain_role.domain_id)

    def test_userdomainrole_list(self):
        objects = []
        for index in range(1, random.randint(5, 20)):
            user_domain_role_data = {
                "role_id": self.role_model.id,
                "domain_id": self.domain_model.id,
                "user_id": "%s" % uuid.uuid1()
            }
            objects.append(db_actions.crud(
                model="UserDomainRole",
                api_model=UserDomainRole,
                data=user_domain_role_data,
                action="create"
            ))

        query_string = [
            ("limit", 2),
            ("role_id", self.role_model.id)
        ]
        response = self.client.open(
            '/api/v1/userdomainroles',
            method='GET',
            query_string=query_string,
            headers=self.headers)

        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
