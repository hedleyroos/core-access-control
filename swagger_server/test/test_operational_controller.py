# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.all_user_roles import AllUserRoles
from swagger_server.models.domain_roles import DomainRoles
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestOperationalController(BaseTestCase):
    """ OperationalController integration test stubs """

    def test_get_all_user_roles(self):
        """
        Test case for get_all_user_roles

        
        """
        response = self.client.open('/api/v1/ops/all_user_roles/{user_id}/'.format(user_id='user_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_domain_roles(self):
        """
        Test case for get_domain_roles

        
        """
        response = self.client.open('/api/v1/ops/domain_roles/{domain_id}/'.format(domain_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_site_and_domain_roles(self):
        """
        Test case for get_site_and_domain_roles

        
        """
        response = self.client.open('/api/v1/ops/site_and_domain_roles/{site_id}/'.format(site_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_site_role_labels_aggregated(self):
        """
        Test case for get_site_role_labels_aggregated

        
        """
        response = self.client.open('/api/v1/ops/site_role_labels_aggregated/{site_id}/'.format(site_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_user_site_role_labels_aggregated(self):
        """
        Test case for get_user_site_role_labels_aggregated

        
        """
        response = self.client.open('/api/v1/ops/user_site_role_labels_aggregated/{user_id}/{site_id}/'.format(user_id='user_id_example', site_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
