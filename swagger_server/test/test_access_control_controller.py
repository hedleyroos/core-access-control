# coding: utf-8

from __future__ import absolute_import

import datetime
import uuid

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

from core_access_control import models

class TestAccessControlGet(BaseTestCase):

    def setUp(self):
        db = models.DB
        self.domain = models.Domain(**{
            "name": ("%s" % uuid.uuid4())[:30],
            "description": "a super cool test demain",
        })
        db.session.add(self.domain)
        db.session.commit()

    """AccessControlController integration test stubs"""
    def test_domain_read(self):
        """Test case for domain_read
        """
        response = self.client.open(
            '/api/v1/domains/{domain_id}/'.format(domain_id=self.domain.id),
            method='GET')
        import pdb; pdb.set_trace()
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
