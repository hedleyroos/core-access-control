# coding: utf-8

from __future__ import absolute_import

import random
import uuid

import werkzeug

from flask import json

from access_control.settings import API_KEY_HEADER
from swagger_server.models.user_site_role import UserSiteRole  # noqa: E501
from swagger_server.models.user_site_role_create import UserSiteRoleCreate  # noqa: E501
from swagger_server.models.site_role import SiteRole  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import db_actions


class TestAccessControlRead(BaseTestCase):

    def setUp(self):
        self.role_data = {
            "label": ("%s" % uuid.uuid1())[:30],
            "description": "user_site_role to create",
        }
        self.role_model = db_actions.crud(
            model="Role",
            api_model=Role,
            data=self.role_data,
            action="create"
        )
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
        self.site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "client_id": uuid.uuid1().int>>97,
            "is_active": True,
        }
        self.site_model = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )
        self.site_role_data = {
            "role_id": self.role_model.id,
            "site_id": self.site_model.id,
        }
        self.site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=self.site_role_data,
            action="create"
        )

        self.user_site_role_data = {
            "role_id": self.role_model.id,
            "site_id": self.site_model.id,
            "user_id": "%s" % uuid.uuid1(),
        }
        self.user_site_role_model = db_actions.crud(
            model="UserSiteRole",
            api_model=UserSiteRole,
            data=self.user_site_role_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_user_site_role_create(self):
        """Test case for user_site_role_create
        """
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
        domain_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test domain",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
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
        site_role_data = {
            "role_id": role_model.id,
            "site_id": site_model.id,
        }
        site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=site_role_data,
            action="create"
        )

        data = UserSiteRoleCreate(**{
            "role_id": role_model.id,
            "site_id": site_model.id,
            "user_id": "%s" % uuid.uuid1(),
        })
        response = self.client.open(
            '/api/v1/usersiteroles',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], data.role_id)
        self.assertEqual(r_data["site_id"], data.site_id)

    def test_user_site_role_read(self):
        """Test case for user_site_role_read
        """
        response = self.client.open(
            '/api/v1/usersiteroles/{user_id}/{site_id}/{role_id}'.format(
                user_id=self.user_site_role_model.user_id,
                site_id=self.user_site_role_model.site_id,
                role_id=self.user_site_role_model.role_id,
            ),
            method='GET',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["role_id"], self.user_site_role_model.role_id)
        self.assertEqual(r_data["site_id"], self.user_site_role_model.site_id)

    def test_user_site_role_delete(self):
        """Test case for user_site_role_delete
        """
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
        domain_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "user_site_role to create",
        }
        domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )
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
        site_role_data = {
            "role_id": role_model.id,
            "site_id": site_model.id,
        }
        site_role_model = db_actions.crud(
            model="SiteRole",
            api_model=SiteRole,
            data=site_role_data,
            action="create"
        )

        user_site_role_data = {
            "role_id": role_model.id,
            "site_id": site_model.id,
            "user_id": "%s" % uuid.uuid1(),
        }
        model = db_actions.crud(
            model="UserSiteRole",
            api_model=UserSiteRole,
            data=user_site_role_data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/usersiteroles/{user_id}/{site_id}/{role_id}'.format(
                user_id=model.user_id,
                site_id=model.site_id,
                role_id=model.role_id,
            ),
            method='DELETE',
            headers=self.headers)

        # Little crude. Raise an error if the object actually still exists else
        # pass after the 404 error.
        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                action="read",
                query={
                    "role_id": model.role_id,
                    "site_id": model.site_id,
                }
            )

    def test_user_site_role_list(self):
        """Test case for user_site_role_list
        """
        objects = []
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
        for index in range(1, random.randint(5, 20)):
            domain_data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "user_site_role to create",
            }
            domain_model = db_actions.crud(
                model="Domain",
                api_model=Domain,
                data=domain_data,
                action="create"
            )
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
            site_role_data = {
                "role_id": role_model.id,
                "site_id": site_model.id,
            }
            site_role_model = db_actions.crud(
                model="SiteRole",
                api_model=SiteRole,
                data=site_role_data,
                action="create"
            )

            user_site_role_data = {
                "role_id": role_model.id,
                "site_id": site_model.id,
                "user_id": "%s" % uuid.uuid1(),
            }
            objects.append(db_actions.crud(
                model="UserSiteRole",
                api_model=UserSiteRole,
                data=user_site_role_data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/usersiteroles',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [#('offset', 0),
                        ('limit', 2),
                        ('role_id', role_model.id),
        ]
        response = self.client.open(
            '/api/v1/usersiteroles',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    #def test_user_site_role_update(self):
    #    """Test case for user_site_role_update
    #    """
    #    role_data = {
    #        "label": ("%s" % uuid.uuid1())[:30],
    #        "description": "user_site_role to create",
    #    }
    #    role_model = db_actions.crud(
    #        model="Role",
    #        api_model=Role,
    #        data=role_data,
    #        action="create"
    #    )
    #    domain_data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "description": "user_site_role to create",
    #    }
    #    domain_model = db_actions.crud(
    #        model="Domain",
    #        api_model=Domain,
    #        data=domain_data,
    #        action="create"
    #    )
    #    site_data = {
    #        "name": ("%s" % uuid.uuid1())[:30],
    #        "domain_id": domain_model.id,
    #        "description": "a super cool test site",
    #        "client_id": uuid.uuid1().int>>97,
    #        "is_active": True,
    #    }
    #    site_model = db_actions.crud(
    #        model="Site",
    #        api_model=Site,
    #        data=site_data,
    #        action="create"
    #    )
    #    site_role_data = {
    #        "role_id": role_model.id,
    #        "site_id": site_model.id,
    #    }
    #    site_role_model = db_actions.crud(
    #        model="SiteRole",
    #        api_model=SiteRole,
    #        data=site_role_data,
    #        action="create"
    #    )
    #    user_site_role_data = {
    #        "role_id": role_model.id,
    #        "site_id": site_model.id,
    #        "user_id": "%s" % uuid.uuid1(),
    #    }
    #    user_site_role_model = db_actions.crud(
    #        model="UserSiteRole",
    #        api_model=UserSiteRole,
    #        data=user_site_role_data,
    #        action="create"
    #    )

    #    # Change user_id on the model.
    #    data = {
    #        "user_id": "%s" % uuid.uuid1(),
    #    }
    #    data = UserSiteRoleCreate(
    #        **data
    #    )
    #    response = self.client.open(
    #        '/api/v1/usersiteroles/{user_id}/{site_id}/{role_id}'.format(
    #            user_id=user_site_role_model.user_id,
    #            site_id=user_site_role_model.site_id,
    #            role_id=user_site_role_model.role_id,
    #        ),
    #        method='PUT',
    #        data=json.dumps(data),
    #        content_type='application/json')
    #    r_data = json.loads(response.data)
    #    updated_entry = db_actions.crud(
    #        model="UserSiteRole",
    #        api_model=UserSiteRole,
    #        action="read",
    #        query={
    #            "role_id": user_site_role_model.role_id,
    #            "site_id": user_site_role_model.site_id,
    #        }
    #    )
    #    self.assertEqual(r_data["user_id"], updated_entry.user_id)
