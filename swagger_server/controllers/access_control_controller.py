import connexion
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
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def access_control_roleresourcepermission_delete(role_id, resource_id, permission_id):
    """
    access_control_roleresourcepermission_delete
    
    :param role_id: A unique integer value identifying the role.
    :type role_id: int
    :param resource_id: A unique integer value identifying the resource.
    :type resource_id: int
    :param permission_id: A unique integer value identifying the permission.
    :type permission_id: int

    :rtype: None
    """
    return 'do some magic!'


def domain_create(data=None):
    """
    domain_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Domain
    """
    if connexion.request.is_json:
        data = Domain.from_dict(connexion.request.get_json())
    return 'do some magic!'


def domain_delete(domain_id):
    """
    domain_delete
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: None
    """
    return 'do some magic!'


def domain_list(offset=None, limit=None, domain_ids=None):
    """
    domain_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param domain_ids: An optional list of domain ids
    :type domain_ids: List[int]

    :rtype: List[Domain]
    """
    return 'do some magic!'


def domain_read(domain_id):
    """
    domain_read
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: Domain
    """
    return 'do some magic!'


def domain_update(domain_id, data=None):
    """
    domain_update
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: Domain
    """
    if connexion.request.is_json:
        data = DomainUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def domainrole_create(data=None):
    """
    domainrole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: DomainRole
    """
    if connexion.request.is_json:
        data = DomainRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def domainrole_delete(domain_id, role_id):
    """
    domainrole_delete
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def domainrole_list(offset=None, limit=None, domain_id=None, role_id=None):
    """
    domainrole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param domain_id: An optional query parameter to filter by domain_id
    :type domain_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[DomainRole]
    """
    return 'do some magic!'


def domainrole_read(domain_id, role_id):
    """
    domainrole_read
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: DomainRole
    """
    return 'do some magic!'


def domainrole_update(domain_id, role_id, data=None):
    """
    domainrole_update
    
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: DomainRole
    """
    if connexion.request.is_json:
        data = DomainRoleUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def invitation_create(data=None):
    """
    invitation_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Invitation
    """
    if connexion.request.is_json:
        data = Invitation.from_dict(connexion.request.get_json())
    return 'do some magic!'


def invitation_delete(invitation_id):
    """
    invitation_delete
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str

    :rtype: None
    """
    return 'do some magic!'


def invitation_list(offset=None, limit=None, invitor_id=None, invitation_ids=None):
    """
    invitation_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param invitor_id: Optional filter based on the invitor (the user who created the invitation)
    :type invitor_id: str
    :param invitation_ids: An optional list of invitation ids
    :type invitation_ids: List[str]

    :rtype: List[Invitation]
    """
    return 'do some magic!'


def invitation_read(invitation_id):
    """
    invitation_read
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str

    :rtype: Invitation
    """
    return 'do some magic!'


def invitation_redeem(invitation_id, user_id):
    """
    invitation_redeem
    Assign all roles assigned to the invitation to the specified user, removing the invitation and related configuration when done. Note: We may have to change the role assignment to an asynchronous task depending on the complexity of the implementation.
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param user_id: A UUID value identifying the user.
    :type user_id: str

    :rtype: AllUserRoles
    """
    return 'do some magic!'


def invitation_update(invitation_id, data=None):
    """
    invitation_update
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param data: 
    :type data: dict | bytes

    :rtype: Invitation
    """
    if connexion.request.is_json:
        data = InvitationUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def invitationdomainrole_create(data=None):
    """
    invitationdomainrole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: InvitationDomainRole
    """
    if connexion.request.is_json:
        data = InvitationDomainRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def invitationdomainrole_delete(invitation_id, domain_id, role_id):
    """
    invitationdomainrole_delete
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def invitationdomainrole_list(offset=None, limit=None, invitation_id=None, domain_id=None, role_id=None):
    """
    invitationdomainrole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param invitation_id: An optional query parameter to filter by invitation_id
    :type invitation_id: str
    :param domain_id: An optional query parameter to filter by domain_id
    :type domain_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[InvitationDomainRole]
    """
    return 'do some magic!'


def invitationdomainrole_read(invitation_id, domain_id, role_id):
    """
    invitationdomainrole_read
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: InvitationDomainRole
    """
    return 'do some magic!'


def invitationsiterole_create(data=None):
    """
    invitationsiterole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: InvitationSiteRole
    """
    if connexion.request.is_json:
        data = InvitationSiteRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def invitationsiterole_delete(invitation_id, site_id, role_id):
    """
    invitationsiterole_delete
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def invitationsiterole_list(offset=None, limit=None, invitation_id=None, site_id=None, role_id=None):
    """
    invitationsiterole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param invitation_id: An optional query parameter to filter by invitation_id
    :type invitation_id: str
    :param site_id: An optional query parameter to filter by site_id
    :type site_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[InvitationSiteRole]
    """
    return 'do some magic!'


def invitationsiterole_read(invitation_id, site_id, role_id):
    """
    invitationsiterole_read
    
    :param invitation_id: A UUID value identifying the invitation.
    :type invitation_id: str
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: InvitationSiteRole
    """
    return 'do some magic!'


def permission_create(data=None):
    """
    permission_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Permission
    """
    if connexion.request.is_json:
        data = Permission.from_dict(connexion.request.get_json())
    return 'do some magic!'


def permission_delete(permission_id):
    """
    permission_delete
    
    :param permission_id: A unique integer value identifying the permission.
    :type permission_id: int

    :rtype: None
    """
    return 'do some magic!'


def permission_list(offset=None, limit=None, permission_ids=None):
    """
    permission_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param permission_ids: An optional list of permission ids
    :type permission_ids: List[int]

    :rtype: List[Permission]
    """
    return 'do some magic!'


def permission_read(permission_id):
    """
    permission_read
    
    :param permission_id: A unique integer value identifying the permission.
    :type permission_id: int

    :rtype: Permission
    """
    return 'do some magic!'


def permission_update(permission_id, data=None):
    """
    permission_update
    
    :param permission_id: A unique integer value identifying the permission.
    :type permission_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: Permission
    """
    if connexion.request.is_json:
        data = PermissionUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def resource_create(data=None):
    """
    resource_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Resource
    """
    if connexion.request.is_json:
        data = Resource.from_dict(connexion.request.get_json())
    return 'do some magic!'


def resource_delete(resource_id):
    """
    resource_delete
    
    :param resource_id: A unique integer value identifying the resource.
    :type resource_id: int

    :rtype: None
    """
    return 'do some magic!'


def resource_list(offset=None, limit=None, prefix=None, resource_ids=None):
    """
    resource_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param prefix: An optional URN prefix filter
    :type prefix: str
    :param resource_ids: An optional list of resource ids
    :type resource_ids: List[int]

    :rtype: List[Resource]
    """
    return 'do some magic!'


def resource_read(resource_id):
    """
    resource_read
    
    :param resource_id: A unique integer value identifying the resource.
    :type resource_id: int

    :rtype: Resource
    """
    return 'do some magic!'


def resource_update(resource_id, data=None):
    """
    resource_update
    
    :param resource_id: A unique integer value identifying the resource.
    :type resource_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: Resource
    """
    if connexion.request.is_json:
        data = ResourceUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def role_create(data=None):
    """
    role_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Role
    """
    if connexion.request.is_json:
        data = Role.from_dict(connexion.request.get_json())
    return 'do some magic!'


def role_delete(role_id):
    """
    role_delete
    
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def role_list(offset=None, limit=None, role_ids=None):
    """
    role_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param role_ids: An optional list of role ids
    :type role_ids: List[int]

    :rtype: List[Role]
    """
    return 'do some magic!'


def role_read(role_id):
    """
    role_read
    
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: Role
    """
    return 'do some magic!'


def role_update(role_id, data=None):
    """
    role_update
    
    :param role_id: A unique integer value identifying the role.
    :type role_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: Role
    """
    if connexion.request.is_json:
        data = RoleUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def roleresourcepermission_create(data=None):
    """
    roleresourcepermission_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: RoleResourcePermission
    """
    if connexion.request.is_json:
        data = RoleResourcePermission.from_dict(connexion.request.get_json())
    return 'do some magic!'


def roleresourcepermission_list(offset=None, limit=None, role_id=None, resource_id=None, permission_id=None):
    """
    roleresourcepermission_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int
    :param resource_id: An optional resource filter
    :type resource_id: int
    :param permission_id: An optional permission filter
    :type permission_id: int

    :rtype: List[RoleResourcePermission]
    """
    return 'do some magic!'


def roleresourcepermission_read(role_id, resource_id, permission_id):
    """
    roleresourcepermission_read
    
    :param role_id: A unique integer value identifying the role.
    :type role_id: int
    :param resource_id: A unique integer value identifying the resource.
    :type resource_id: int
    :param permission_id: A unique integer value identifying the permission.
    :type permission_id: int

    :rtype: RoleResourcePermission
    """
    return 'do some magic!'


def site_create(data=None):
    """
    site_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: Site
    """
    if connexion.request.is_json:
        data = Site.from_dict(connexion.request.get_json())
    return 'do some magic!'


def site_delete(site_id):
    """
    site_delete
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: None
    """
    return 'do some magic!'


def site_list(offset=None, limit=None, site_ids=None):
    """
    site_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param site_ids: An optional list of site ids
    :type site_ids: List[int]

    :rtype: List[Site]
    """
    return 'do some magic!'


def site_read(site_id):
    """
    site_read
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: Site
    """
    return 'do some magic!'


def site_update(site_id, data=None):
    """
    site_update
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: Site
    """
    if connexion.request.is_json:
        data = SiteUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def siterole_create(data=None):
    """
    siterole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: SiteRole
    """
    if connexion.request.is_json:
        data = SiteRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def siterole_delete(site_id, role_id):
    """
    siterole_delete
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def siterole_list(offset=None, limit=None, site_id=None, role_id=None):
    """
    siterole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param site_id: An optional query parameter to filter by site_id
    :type site_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[SiteRole]
    """
    return 'do some magic!'


def siterole_read(site_id, role_id):
    """
    siterole_read
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: SiteRole
    """
    return 'do some magic!'


def siterole_update(site_id, role_id, data=None):
    """
    siterole_update
    
    :param site_id: A unique integer value identifying the site.
    :type site_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int
    :param data: 
    :type data: dict | bytes

    :rtype: SiteRole
    """
    if connexion.request.is_json:
        data = SiteRoleUpdate.from_dict(connexion.request.get_json())
    return 'do some magic!'


def userdomainrole_create(data=None):
    """
    userdomainrole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: UserDomainRole
    """
    if connexion.request.is_json:
        data = UserDomainRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def userdomainrole_delete(user_id, domain_id, role_id):
    """
    userdomainrole_delete
    
    :param user_id: A UUID value identifying the user.
    :type user_id: str
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: None
    """
    return 'do some magic!'


def userdomainrole_list(offset=None, limit=None, user_id=None, domain_id=None, role_id=None):
    """
    userdomainrole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param user_id: An optional query parameter to filter by user_id
    :type user_id: str
    :param domain_id: An optional query parameter to filter by domain_id
    :type domain_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[UserDomainRole]
    """
    return 'do some magic!'


def userdomainrole_read(user_id, domain_id, role_id):
    """
    userdomainrole_read
    
    :param user_id: A UUID value identifying the user.
    :type user_id: str
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int
    :param role_id: A unique integer value identifying the role.
    :type role_id: int

    :rtype: UserDomainRole
    """
    return 'do some magic!'


def usersiterole_create(data=None):
    """
    usersiterole_create
    
    :param data: 
    :type data: dict | bytes

    :rtype: UserSiteRole
    """
    if connexion.request.is_json:
        data = UserSiteRole.from_dict(connexion.request.get_json())
    return 'do some magic!'


def usersiterole_list(offset=None, limit=None, user_id=None, site_id=None, role_id=None):
    """
    usersiterole_list
    
    :param offset: An optional query parameter specifying the offset in the result set to start from.
    :type offset: int
    :param limit: An optional query parameter to limit the number of results returned.
    :type limit: int
    :param user_id: An optional query parameter to filter by user_id
    :type user_id: str
    :param site_id: An optional query parameter to filter by site_id
    :type site_id: int
    :param role_id: An optional query parameter to filter by role_id
    :type role_id: int

    :rtype: List[UserSiteRole]
    """
    return 'do some magic!'
