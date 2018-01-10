# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.all_user_roles import AllUserRoles
from swagger_server.models.domain import Domain
from swagger_server.models.domain_role import DomainRole
from swagger_server.models.domain_role_update import DomainRoleUpdate
from swagger_server.models.domain_update import DomainUpdate
from swagger_server.models.invitation import Invitation
from swagger_server.models.invitation_domain_role import InvitationDomainRole
from swagger_server.models.invitation_site_role import InvitationSiteRole
from swagger_server.models.invitation_update import InvitationUpdate
from swagger_server.models.permission import Permission
from swagger_server.models.permission_update import PermissionUpdate
from swagger_server.models.resource import Resource
from swagger_server.models.resource_update import ResourceUpdate
from swagger_server.models.role import Role
from swagger_server.models.role_resource_permission import RoleResourcePermission
from swagger_server.models.role_update import RoleUpdate
from swagger_server.models.site import Site
from swagger_server.models.site_role import SiteRole
from swagger_server.models.site_role_update import SiteRoleUpdate
from swagger_server.models.site_update import SiteUpdate
from swagger_server.models.user_domain_role import UserDomainRole
from swagger_server.models.user_site_role import UserSiteRole
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestAccessControlController(BaseTestCase):
    """ AccessControlController integration test stubs """

    def test_access_control_roleresourcepermission_delete(self):
        """
        Test case for access_control_roleresourcepermission_delete

        
        """
        response = self.client.open('/api/v1/roleresourcepermissions/{role_id}/{resource_id}/{permission_id}/'.format(role_id=56, resource_id=56, permission_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domain_create(self):
        """
        Test case for domain_create

        
        """
        data = Domain()
        response = self.client.open('/api/v1/domains/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domain_delete(self):
        """
        Test case for domain_delete

        
        """
        response = self.client.open('/api/v1/domains/{domain_id}/'.format(domain_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domain_list(self):
        """
        Test case for domain_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('domain_ids', 56)]
        response = self.client.open('/api/v1/domains/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domain_read(self):
        """
        Test case for domain_read

        
        """
        response = self.client.open('/api/v1/domains/{domain_id}/'.format(domain_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domain_update(self):
        """
        Test case for domain_update

        
        """
        data = DomainUpdate()
        response = self.client.open('/api/v1/domains/{domain_id}/'.format(domain_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domainrole_create(self):
        """
        Test case for domainrole_create

        
        """
        data = DomainRole()
        response = self.client.open('/api/v1/domainroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domainrole_delete(self):
        """
        Test case for domainrole_delete

        
        """
        response = self.client.open('/api/v1/domainroles/{domain_id}/{role_id}/'.format(domain_id=56, role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domainrole_list(self):
        """
        Test case for domainrole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('domain_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/domainroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domainrole_read(self):
        """
        Test case for domainrole_read

        
        """
        response = self.client.open('/api/v1/domainroles/{domain_id}/{role_id}/'.format(domain_id=56, role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_domainrole_update(self):
        """
        Test case for domainrole_update

        
        """
        data = DomainRoleUpdate()
        response = self.client.open('/api/v1/domainroles/{domain_id}/{role_id}/'.format(domain_id=56, role_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_create(self):
        """
        Test case for invitation_create

        
        """
        data = Invitation()
        response = self.client.open('/api/v1/invitations/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_delete(self):
        """
        Test case for invitation_delete

        
        """
        response = self.client.open('/api/v1/invitations/{invitation_id}/'.format(invitation_id='invitation_id_example'),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_list(self):
        """
        Test case for invitation_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('invitor_id', 'invitor_id_example'),
                        ('invitation_ids', 'invitation_ids_example')]
        response = self.client.open('/api/v1/invitations/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_read(self):
        """
        Test case for invitation_read

        
        """
        response = self.client.open('/api/v1/invitations/{invitation_id}/'.format(invitation_id='invitation_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_redeem(self):
        """
        Test case for invitation_redeem

        
        """
        response = self.client.open('/api/v1/invitations/{invitation_id}/redeem/{user_id}/'.format(invitation_id='invitation_id_example', user_id='user_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitation_update(self):
        """
        Test case for invitation_update

        
        """
        data = InvitationUpdate()
        response = self.client.open('/api/v1/invitations/{invitation_id}/'.format(invitation_id='invitation_id_example'),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationdomainrole_create(self):
        """
        Test case for invitationdomainrole_create

        
        """
        data = InvitationDomainRole()
        response = self.client.open('/api/v1/invitationdomainroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationdomainrole_delete(self):
        """
        Test case for invitationdomainrole_delete

        
        """
        response = self.client.open('/api/v1/invitationdomainroles/{invitation_id}/{domain_id}/{role_id}'.format(invitation_id='invitation_id_example', domain_id=56, role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationdomainrole_list(self):
        """
        Test case for invitationdomainrole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('invitation_id', 'invitation_id_example'),
                        ('domain_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/invitationdomainroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationdomainrole_read(self):
        """
        Test case for invitationdomainrole_read

        
        """
        response = self.client.open('/api/v1/invitationdomainroles/{invitation_id}/{domain_id}/{role_id}'.format(invitation_id='invitation_id_example', domain_id=56, role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationsiterole_create(self):
        """
        Test case for invitationsiterole_create

        
        """
        data = InvitationSiteRole()
        response = self.client.open('/api/v1/invitationsiteroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationsiterole_delete(self):
        """
        Test case for invitationsiterole_delete

        
        """
        response = self.client.open('/api/v1/invitationsiteroles/{invitation_id}/{site_id}/{role_id}'.format(invitation_id='invitation_id_example', site_id=56, role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationsiterole_list(self):
        """
        Test case for invitationsiterole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('invitation_id', 'invitation_id_example'),
                        ('site_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/invitationsiteroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invitationsiterole_read(self):
        """
        Test case for invitationsiterole_read

        
        """
        response = self.client.open('/api/v1/invitationsiteroles/{invitation_id}/{site_id}/{role_id}'.format(invitation_id='invitation_id_example', site_id=56, role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_permission_create(self):
        """
        Test case for permission_create

        
        """
        data = Permission()
        response = self.client.open('/api/v1/permissions/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_permission_delete(self):
        """
        Test case for permission_delete

        
        """
        response = self.client.open('/api/v1/permissions/{permission_id}/'.format(permission_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_permission_list(self):
        """
        Test case for permission_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('permission_ids', 56)]
        response = self.client.open('/api/v1/permissions/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_permission_read(self):
        """
        Test case for permission_read

        
        """
        response = self.client.open('/api/v1/permissions/{permission_id}/'.format(permission_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_permission_update(self):
        """
        Test case for permission_update

        
        """
        data = PermissionUpdate()
        response = self.client.open('/api/v1/permissions/{permission_id}/'.format(permission_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_resource_create(self):
        """
        Test case for resource_create

        
        """
        data = Resource()
        response = self.client.open('/api/v1/resources/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_resource_delete(self):
        """
        Test case for resource_delete

        
        """
        response = self.client.open('/api/v1/resources/{resource_id}/'.format(resource_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_resource_list(self):
        """
        Test case for resource_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('prefix', 'prefix_example'),
                        ('resource_ids', 56)]
        response = self.client.open('/api/v1/resources/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_resource_read(self):
        """
        Test case for resource_read

        
        """
        response = self.client.open('/api/v1/resources/{resource_id}/'.format(resource_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_resource_update(self):
        """
        Test case for resource_update

        
        """
        data = ResourceUpdate()
        response = self.client.open('/api/v1/resources/{resource_id}/'.format(resource_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_role_create(self):
        """
        Test case for role_create

        
        """
        data = Role()
        response = self.client.open('/api/v1/roles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_role_delete(self):
        """
        Test case for role_delete

        
        """
        response = self.client.open('/api/v1/roles/{role_id}/'.format(role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_role_list(self):
        """
        Test case for role_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('role_ids', 56)]
        response = self.client.open('/api/v1/roles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_role_read(self):
        """
        Test case for role_read

        
        """
        response = self.client.open('/api/v1/roles/{role_id}/'.format(role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_role_update(self):
        """
        Test case for role_update

        
        """
        data = RoleUpdate()
        response = self.client.open('/api/v1/roles/{role_id}/'.format(role_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_roleresourcepermission_create(self):
        """
        Test case for roleresourcepermission_create

        
        """
        data = RoleResourcePermission()
        response = self.client.open('/api/v1/roleresourcepermissions/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_roleresourcepermission_list(self):
        """
        Test case for roleresourcepermission_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('role_id', 56),
                        ('resource_id', 56),
                        ('permission_id', 56)]
        response = self.client.open('/api/v1/roleresourcepermissions/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_roleresourcepermission_read(self):
        """
        Test case for roleresourcepermission_read

        
        """
        response = self.client.open('/api/v1/roleresourcepermissions/{role_id}/{resource_id}/{permission_id}/'.format(role_id=56, resource_id=56, permission_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_site_create(self):
        """
        Test case for site_create

        
        """
        data = Site()
        response = self.client.open('/api/v1/sites/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_site_delete(self):
        """
        Test case for site_delete

        
        """
        response = self.client.open('/api/v1/sites/{site_id}/'.format(site_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_site_list(self):
        """
        Test case for site_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('site_ids', 56)]
        response = self.client.open('/api/v1/sites/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_site_read(self):
        """
        Test case for site_read

        
        """
        response = self.client.open('/api/v1/sites/{site_id}/'.format(site_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_site_update(self):
        """
        Test case for site_update

        
        """
        data = SiteUpdate()
        response = self.client.open('/api/v1/sites/{site_id}/'.format(site_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_siterole_create(self):
        """
        Test case for siterole_create

        
        """
        data = SiteRole()
        response = self.client.open('/api/v1/siteroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_siterole_delete(self):
        """
        Test case for siterole_delete

        
        """
        response = self.client.open('/api/v1/siteroles/{site_id}/{role_id}/'.format(site_id=56, role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_siterole_list(self):
        """
        Test case for siterole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('site_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/siteroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_siterole_read(self):
        """
        Test case for siterole_read

        
        """
        response = self.client.open('/api/v1/siteroles/{site_id}/{role_id}/'.format(site_id=56, role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_siterole_update(self):
        """
        Test case for siterole_update

        
        """
        data = SiteRoleUpdate()
        response = self.client.open('/api/v1/siteroles/{site_id}/{role_id}/'.format(site_id=56, role_id=56),
                                    method='PUT',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_userdomainrole_create(self):
        """
        Test case for userdomainrole_create

        
        """
        data = UserDomainRole()
        response = self.client.open('/api/v1/userdomainroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_userdomainrole_delete(self):
        """
        Test case for userdomainrole_delete

        
        """
        response = self.client.open('/api/v1/userdomainroles/{user_id}/{domain_id}/{role_id}/'.format(user_id='user_id_example', domain_id=56, role_id=56),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_userdomainrole_list(self):
        """
        Test case for userdomainrole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('user_id', 'user_id_example'),
                        ('domain_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/userdomainroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_userdomainrole_read(self):
        """
        Test case for userdomainrole_read

        
        """
        response = self.client.open('/api/v1/userdomainroles/{user_id}/{domain_id}/{role_id}/'.format(user_id='user_id_example', domain_id=56, role_id=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_usersiterole_create(self):
        """
        Test case for usersiterole_create

        
        """
        data = UserSiteRole()
        response = self.client.open('/api/v1/usersiteroles/',
                                    method='POST',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_usersiterole_list(self):
        """
        Test case for usersiterole_list

        
        """
        query_string = [('offset', 1),
                        ('limit', 100),
                        ('user_id', 'user_id_example'),
                        ('site_id', 56),
                        ('role_id', 56)]
        response = self.client.open('/api/v1/usersiteroles/',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
