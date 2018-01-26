# coding: utf-8

from __future__ import absolute_import

import datetime
import random
import uuid
import werkzeug

from flask import json
from six import BytesIO

from swagger_server.models.all_user_roles import AllUserRoles  # noqa: E501
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.domain_role import DomainRole  # noqa: E501
from swagger_server.models.domain_role_update import DomainRoleUpdate  # noqa: E501
from swagger_server.models.domain_update import DomainUpdate  # noqa: E501
from swagger_server.models.invitation import Invitation  # noqa: E501
from swagger_server.models.invitation_domain_role import InvitationDomainRole  # noqa: E501
from swagger_server.models.invitation_site_role import InvitationSiteRole  # noqa: E501
from swagger_server.models.invitation_update import InvitationUpdate  # noqa: E501
from swagger_server.models.permission import Permission  # noqa: E501
from swagger_server.models.permission_update import PermissionUpdate  # noqa: E501
from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server.models.resource_update import ResourceUpdate  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.role_resource_permission import RoleResourcePermission  # noqa: E501
from swagger_server.models.role_update import RoleUpdate  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.site_role import SiteRole  # noqa: E501
from swagger_server.models.site_role_update import SiteRoleUpdate  # noqa: E501
from swagger_server.models.site_update import SiteUpdate  # noqa: E501
from swagger_server.models.user_domain_role import UserDomainRole  # noqa: E501
from swagger_server.models.user_site_role import UserSiteRole  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import models, db_actions


class TestAccessControlRead(BaseTestCase):

    def setUp(self):
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

    def test_domain_create(self):
        """Test case for domainrole_create
        """
        data = Domain(**{
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "Domain to create",
        })
        response = self.client.open(
            '/api/v1/domains/',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], data.name)
        self.assertEqual(r_data["description"], data.description)


    def test_domain_read(self):
        """Test case for domain_read
        """
        response = self.client.open(
            '/api/v1/domains/{domain_id}/'.format(domain_id=self.domain_model.id),
            method='GET')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], self.domain_model.name)
        self.assertEqual(r_data["description"], self.domain_model.description)
        self.assertEqual(r_data["id"], self.domain_model.id)

    def test_domain_delete(self):
        """Test case for domain_delete
        """
        data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "Domain to delete",
        }
        model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/domains/{domain_id}/'.format(domain_id=model.id),
            method='DELETE')

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Domain",
                api_model=Domain,
                action="read",
                query={"id": model.id}
            )

    def test_domain_list(self):
        """Test case for domain_list
        """
        objects = []
        for index in range(3, random.randint(4, 20)):
            data = {
                "name": ("%s" % uuid.uuid4())[:30],
                "description": "Domain list %s" % index,
            }
            objects.append(db_actions.crud(
                model="Domain",
                api_model=Domain,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('domain_ids', ",".join(map(str, [domain.id for domain in objects])))]
        response = self.client.open(
            '/api/v1/domains/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [('limit', 2),
                        ('domain_ids', ",".join(map(str, [domain.id for domain in objects])))]
        response = self.client.open(
            '/api/v1/domains/',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_domain_update(self):
        """Test case for domain_update
        """
        data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "Domain to update",
        }
        model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=data,
            action="create"
        )
        data = {
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "Domain updated",
        }
        data = DomainUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/domains/{domain_id}/'.format(domain_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Domain",
            api_model=Domain,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["name"], updated_entry.name)
        self.assertEqual(r_data["description"], updated_entry.description)
