"""
Initial permissions on resources assigned to roles, based on this document:
https://praekelt.atlassian.net/wiki/spaces/GEM/pages/55574535/Global+Management+Portal+Access+Roles+and+Permissions+Matrix
"""
ROLE_RESOURCE_PERMISSIONS = {
    # Do not define any permissions for the "tech_admin" role
    "role_delegator": [
        # Assign/remove roles to/from users
        ("urn:ge:access_control:userdomainrole", "create"),
        ("urn:ge:access_control:userdomainrole", "read"),
        ("urn:ge:access_control:userdomainrole", "delete"),
        ("urn:ge:access_control:usersiterole", "create"),
        ("urn:ge:access_control:usersiterole", "read"),
        ("urn:ge:access_control:userdomainrole", "delete"),
        # Search for users
        ("urn:ge:identity_provider:user", "read"),
        # Invite a user
        ("urn:ge:access_control:invitation", "create"),
        ("urn:ge:access_control:invitation", "read"),
        ("urn:ge:access_control:invitation", "update"),
        ("urn:ge:access_control:invitation", "delete"),
        ("urn:ge:access_control:invitationdomainrole", "create"),
        ("urn:ge:access_control:invitationdomainrole", "read"),
        ("urn:ge:access_control:invitationdomainrole", "update"),
        ("urn:ge:access_control:invitationdomainrole", "delete"),
        ("urn:ge:access_control:invitationsiterole", "create"),
        ("urn:ge:access_control:invitationsiterole", "read"),
        ("urn:ge:access_control:invitationsiterole", "update"),
        ("urn:ge:access_control:invitationsiterole", "delete"),
    ],
    "governance_admin": [
        ("urn:ge:identity_provider:user", "read"),
        ("urn:ge:identity_provider:user", "update"),
        ("urn:ge:identity_provider:user", "delete"),
        ("urn:ge:management_portal:users:export", "create"),
    ],
    "governance_viewer": [
        ("urn:ge:identity_provider:user", "read"),
        ("urn:ge:management_portal:users:export", "create"),
    ],
    "data_admin": [
        ("urn:ge:identity_provider:user", "read"),
        ("urn:ge:identity_provider:user", "update"),
        ("urn:ge:identity_provider:user", "delete"),
        ("urn:ge:management_portal:users:export", "create"),
    ],
    "data_editor": [
        ("urn:ge:identity_provider:user", "read"),
        ("urn:ge:management_portal:users:export", "create"),
    ],
    "data_viewer": [
        ("urn:ge:identity_provider:user", "read"),
    ],
    "content_admin": [
        ("urn:ge:identity_provider:user", "read"),
    ],
    "content_editor": [
        # No permissions defined
    ],
    "content_viewer": [
        # No permissions defined
    ],
}
