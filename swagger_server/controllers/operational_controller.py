import connexion
import datetime
import socket

from sqlalchemy import text

import project.app
from access_control import __version__

from swagger_server.models.all_user_roles import AllUserRoles  # noqa: E501
from swagger_server.models.domain_roles import DomainRoles  # noqa: E501
from swagger_server.models.health_info import HealthInfo  # noqa: E501
from swagger_server.models.purged_invitations import PurgedInvitations  # noqa: E501
from swagger_server.models.resource_permission import ResourcePermission  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles  # noqa: E501
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_deletion_data import UserDeletionData  # noqa: E501
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_with_roles import UserWithRoles  # noqa: E501

db = project.app.DB

SQL_ALL_DOMAIN_ROLES_FOR_USER = """
-- Given a user id (:user_id), find all roles in the organisational domain tree

-- Finding all the implicit and explicit roles is simple,
-- however, we need to return the results in such a way
-- that the domain hierarchy can be interpreted and roles
-- pushed down the tree.

WITH RECURSIVE _domain_tree AS (
  SELECT domain.id, domain.parent_id, 0 AS position
    FROM domain
   WHERE domain.parent_id IS NULL  -- The root domain
   UNION
  SELECT domain.id, domain.parent_id,
         _domain_tree.position + 1 AS position
    FROM _domain_tree,
         domain
   WHERE domain.parent_id = _domain_tree.id
),
_roles AS (
  SELECT domain.id, domain.parent_id,
         -- Domain roles are distinct per definition
         array_agg(domainrole.role_id) AS implicit_roles,
         -- User domain roles are distinct per definition
         array_agg(userdomainrole.role_id) AS explicit_roles
    FROM _domain_tree AS domain
    LEFT OUTER JOIN domain_role AS domainrole
         ON (domain.id = domainrole.domain_id AND
             domainrole.grant_implicitly)
    LEFT OUTER JOIN user_domain_role AS userdomainrole
         ON (domain.id = userdomainrole.domain_id AND
             userdomainrole.user_id = :user_id)
   GROUP BY domain.id, domain.parent_id, domain.position
   ORDER BY domain.position
)
-- Return all the nodes of the tree with the roles for the
-- specified user. The list of roles needs to be post-processed
-- as it may contain duplicates and NULL values, e.g. {6,null} or {null,null}
SELECT id, parent_id, implicit_roles || explicit_roles AS roles
  FROM _roles;
"""

SQL_ALL_RESOURCE_ROLES_FOR_USER = """
WITH _roles AS (
  SELECT site.id, site.domain_id,
         -- Site roles are distinct per definition
         array_agg(siterole.role_id) AS implicit_roles,
         -- User site roles are distinct per definition
         array_agg(userresourcerole.role_id) AS explicit_roles
    FROM site
    LEFT OUTER JOIN site_role AS siterole
      ON (site.id = siterole.site_id AND
          siterole.grant_implicitly)
    LEFT OUTER JOIN user_site_role AS userresourcerole
      ON (site.id = userresourcerole.site_id AND
          userresourcerole.user_id = :user_id)
   GROUP BY site.id, site.domain_id
)
-- Return all the sites with the implicit and explicit
-- roles for the specified user.
-- The list of roles needs to be post-processed as it may contain duplicates and NULL values, e.g.
-- {6,null} or {null,null}
SELECT id, domain_id, implicit_roles || explicit_roles AS roles
  FROM _roles;
"""

SQL_ALL_SITE_ROLES_FOR_USER = """
WITH _roles AS (
  SELECT site.id, site.domain_id,
         -- Site roles are distinct per definition
         array_agg(siterole.role_id) AS implicit_roles,
         -- User site roles are distinct per definition
         array_agg(usersiterole.role_id) AS explicit_roles
    FROM site
    LEFT OUTER JOIN site_role AS siterole
      ON (site.id = siterole.site_id AND
          siterole.grant_implicitly)
    LEFT OUTER JOIN user_site_role AS usersiterole
      ON (site.id = usersiterole.site_id AND
          usersiterole.user_id = :user_id)
   GROUP BY site.id, site.domain_id
)
-- Return all the sites with the implicit and explicit
-- roles for the specified user.
-- The list of roles needs to be post-processed as it may contain duplicates and NULL values, e.g.
-- {6,null} or {null,null}
SELECT id, domain_id, implicit_roles || explicit_roles AS roles
  FROM _roles;
"""

SQL_DOMAIN_ROLES = """
-- Given a domain id (:domain_id), find all roles that can be assigned
-- in the domain lineage

-- Finding all the roles is simple,
-- however, we need to return the results in such a way
-- that the domain hierarchy can be interpreted and roles
-- pushed down the tree.

WITH RECURSIVE _domain_tree AS (
  SELECT domain.id, domain.parent_id, 0 AS position
    FROM domain
   WHERE domain.id = :domain_id
   UNION
  SELECT domain.id, domain.parent_id,
         _domain_tree.position - 1 AS position
    FROM _domain_tree,
         domain
   WHERE _domain_tree.parent_id = domain.id
)
SELECT domain.id, domain.parent_id,
       array_agg(domainrole.role_id) AS roles
  FROM _domain_tree AS domain
  LEFT OUTER JOIN domain_role AS domainrole
    ON (domain.id = domainrole.domain_id)
 GROUP BY domain.id, domain.parent_id, domain.position
 ORDER BY domain.position
"""

SQL_SITE_ROLES = """
-- Given a site id (:site_id), find all roles that can be assigned
-- to it.
SELECT site.id, site.domain_id, array_agg(siterole.role_id) AS roles
FROM site
LEFT OUTER JOIN site_role AS siterole
  ON (site.id = siterole.site_id)
WHERE site.id = :site_id
GROUP BY site.id, site.domain_id
"""

SQL_SITE_ROLE_LABELS_AGGREGATED = """
-- Given a site id (:site_id) find all roles that can be assigned to it
-- directly and via its domain lineage.

-- The recursive query needs to come first
-- Get domain lineage ids
WITH RECURSIVE _domain_lineage AS (
    SELECT domain.id, domain.parent_id
      FROM domain, site
     WHERE domain.id = site.domain_id
       AND site.id = :site_id
     UNION DISTINCT
    SELECT domain.id, domain.parent_id
      FROM domain, _domain_lineage
     WHERE domain.id = _domain_lineage.parent_id
),
-- Find all roles that can be assigned in the domain lineage
_domain_role_ids AS (
    SELECT role_id
      FROM domain_role, _domain_lineage
     WHERE domain_role.domain_id = _domain_lineage.id
),
-- Find all roles that can be assigned for the site
_site_role_ids AS (
    SELECT role_id
      FROM site_role
     WHERE site_role.site_id = :site_id
),
-- Create a list of role ids, potentially containing duplicates
_role_ids AS (
    SELECT * FROM _domain_role_ids
     UNION
    SELECT * FROM _site_role_ids
)
-- Return a set of role labels
-- The order in which the roles are returned is not guaranteed and
-- applications should not rely on it.
SELECT DISTINCT(label)
  FROM role, _role_ids
 WHERE role.id = _role_ids.role_id
"""

SQL_USER_SITE_ROLE_LABELS_AGGREGATED = """
-- Given a site id (:site_id) and a user id (:user_id), find all roles

-- The recursive query needs to come first
-- Get domain lineage ids
WITH RECURSIVE _domain_lineage AS (
    SELECT domain.id, domain.parent_id
      FROM domain, site
     WHERE domain.id = site.domain_id
       AND site.id = :site_id
     UNION DISTINCT
    SELECT domain.id, domain.parent_id
      FROM domain, _domain_lineage
     WHERE domain.id = _domain_lineage.parent_id
),
-- Find all implicit roles defined for the domain lineage
_implicit_domain_role_ids AS (
    SELECT role_id
      FROM domain_role, _domain_lineage
     WHERE domain_role.domain_id = _domain_lineage.id
       AND domain_role.grant_implicitly
),
-- Find all explicit roles defined for the domain lineage
_explicit_domain_role_ids AS (
    SELECT role_id
      FROM user_domain_role, _domain_lineage
     WHERE user_domain_role.domain_id = _domain_lineage.id
       AND user_domain_role.user_id = :user_id
),
-- Find all implicit roles defined for the site
_implicit_site_role_ids AS (
    SELECT role_id
      FROM site_role
     WHERE site_role.site_id = :site_id
       AND site_role.grant_implicitly
),
-- Find all explicit roles defined for the site
_explicit_site_role_ids AS (
    SELECT role_id
      FROM user_site_role
     WHERE user_site_role.site_id = :site_id
       AND user_site_role.user_id = :user_id
),
-- Create a list of role ids, potentially containing duplicates
_role_ids AS (
    SELECT * FROM _implicit_domain_role_ids
     UNION
    SELECT * FROM _explicit_domain_role_ids
     UNION
    SELECT * FROM _implicit_site_role_ids
     UNION
    SELECT * FROM _explicit_site_role_ids
)
-- Return a set of role labels
-- The order in which the roles are returned is not guaranteed and
-- applications should not rely on it.
SELECT DISTINCT(label)
  FROM role, _role_ids
 WHERE role.id = _role_ids.role_id
"""

SQL_USERS_WITH_ROLES_FOR_DOMAIN = """
-- Given a domain_id, find all users and their roles on that domain.

-- We find all the users that has roles in the specified domains lineage
-- in order to get all effective roles the a users have.
WITH RECURSIVE _domain_lineage AS (
  SELECT domain.id, domain.parent_id
    FROM domain
   WHERE domain.id = :domain_id
   UNION
  SELECT domain.id, domain.parent_id
    FROM _domain_lineage, domain
   WHERE domain.id = _domain_lineage.parent_id
)
SELECT user_domain_role.user_id,
       array_agg(DISTINCT user_domain_role.role_id) AS role_ids
  FROM user_domain_role, _domain_lineage AS domain  
 WHERE domain.id = user_domain_role.domain_id
 GROUP BY user_domain_role.user_id;
"""

SQL_USERS_WITH_ROLES_FOR_SITE = """
-- Given a site id (:site_id) find all users and their roles on that site.

-- The recursive query needs to come first
-- Get domain lineage ids
WITH RECURSIVE _domain_lineage AS (
    SELECT domain.id, domain.parent_id
      FROM domain, site
     WHERE domain.id = site.domain_id
       AND site.id = :site_id
     UNION DISTINCT
    SELECT domain.id, domain.parent_id
      FROM domain, _domain_lineage
     WHERE domain.id = _domain_lineage.parent_id
),
_user_roles AS (
    SELECT user_domain_role.user_id, user_domain_role.role_id 
      FROM user_domain_role, _domain_lineage AS domain
     WHERE domain.id = user_domain_role.domain_id
    UNION
    SELECT user_id, role_id
      FROM user_site_role
     WHERE site_id = :site_id
)
SELECT user_id, array_agg(DISTINCT role_id) AS role_ids
  FROM _user_roles
 GROUP BY user_id
"""

SQL_TECH_ADMIN_RESOURCE_PERMISSIONS = """
-- A user with the tech admin role has all permissions on all resources.
-- This is computed as the cross-product between the resource and permission table.
SELECT resource.id AS resource_id, permission.id AS permission_id
  FROM resource, permission
"""

SQL_RESOURCE_PERMISSIONS_FOR_ROLES = """
-- Given a list of roles (:role_ids) find all resource permissions linked to them.
SELECT resource_id, permission_id
  FROM role_resource_permission
 WHERE role_resource_permission.role_id = ANY(:role_ids)
"""

SQL_SITES_UNDER_DOMAIN = """
-- Given a domain id (:domain_id) find all sites linked to it or any of its subdomains.

-- The recursive query needs to come first
-- Get domain ids for the subtree rooted at the domain with id :domain_id
WITH RECURSIVE _domain_tree AS (
    SELECT domain.id
      FROM domain
     WHERE domain.id = :domain_id
     UNION DISTINCT
    SELECT domain.id
      FROM domain, _domain_tree
     WHERE domain.parent_id = _domain_tree.id
)
SELECT site.*
  FROM site, _domain_tree
 WHERE domain_id = _domain_tree.id
"""

SQL_PURGE_EXPIRED_INVITATIONS = """
-- Given a cutoff date (:cutoff_date), find all invitations with an
-- expired_date beyond the cutoff_date and purge them.

-- The InvitationDomainRoles and InvitationSiteRoles must be purged prior to
-- purging the Invitation itself, to avoid errors.
WITH invitations_to_delete AS (
    SELECT id
      FROM invitation
     WHERE expires_at < :cutoff_date
),
deleted_invitation_domain_roles AS (
    DELETE FROM invitation_domain_role
     USING invitations_to_delete
     WHERE invitation_id = invitations_to_delete.id
),
deleted_invitation_site_roles AS (
    DELETE FROM invitation_site_role
     USING invitations_to_delete
     WHERE invitation_id = invitations_to_delete.id
),
deleted_invitations AS (
    DELETE FROM invitation
     USING invitations_to_delete
     WHERE invitation.id = invitations_to_delete.id
    RETURNING * 
)
SELECT COUNT(*) AS amount
  FROM deleted_invitations;
"""

SQL_DELETE_USER_DATA = """
-- Given a user id (:user_id),
-- delete UserDomainRoles, UserResourceRoles and UserSiteRoles tied to user id

WITH deleted_site_roles AS (
    DELETE FROM user_site_role
        WHERE user_id = :user_id
    RETURNING user_id
),
deleted_domain_roles AS (
    DELETE FROM user_domain_role
        WHERE user_id = :user_id
    RETURNING user_id
),
deleted_resource_roles AS (
    DELETE FROM user_resource_role
        WHERE user_id = :user_id
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

def delete_user_data(user_id):  # noqa: E501
    """delete_user_data

     # noqa: E501

    :param user_id: A UUID value identifying the user.
    :type user_id: dict | bytes

    :rtype: UserDeletionData
    """
    with db.session.get_bind().begin() as connection:
        result = connection.execute(
            text(SQL_DELETE_USER_DATA),
            **{"user_id": user_id}
        )

    amount = result.fetchone()["amount"]
    return UserDeletionData(amount=amount)

def get_all_user_roles(user_id):  # noqa: E501
    """get_all_user_roles

    Get the effective roles that a user has at any place in the organisational tree. # noqa: E501

    :param user_id: A UUID value identifying the user.
    :type user_id: dict | bytes

    :rtype: AllUserRoles
    """
    domain_rows = db.session.get_bind().execute(
        text(SQL_ALL_DOMAIN_ROLES_FOR_USER), **{"user_id": user_id}
    )
    site_rows = db.session.get_bind().execute(
        text(SQL_ALL_SITE_ROLES_FOR_USER), **{"user_id": user_id}
    )
    roles = {}
    for row in domain_rows:
        key = "d:%s" % row["id"]
        roles[key] = set(filter(None, row["roles"]))
        if row["parent_id"]:
            # Child domains inherit the roles of their parent
            parent_key = "d:%s" % row["parent_id"]
            roles[key].update(roles[parent_key])

    for row in site_rows:
        key = "s:%s" % row["id"]
        roles[key] = set(filter(None, row["roles"]))
        if row["domain_id"]:
            # Sites inherit the roles of their domain
            parent_key = "d:%s" % row["domain_id"]
            roles[key].update(roles[parent_key])

    # Convert the sets to lists so that they are JSON serialisable
    for k, v in roles.items():
        roles[k] = list(v)

    return AllUserRoles(**{"roles_map": roles, "user_id": user_id})


def get_domain_roles(domain_id):  # noqa: E501
    """get_domain_roles

    Get the domain and its lineage&#39;s roles defined for a domain. # noqa: E501

    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: DomainRoles
    """
    result = db.session.get_bind().execute(
        text(SQL_DOMAIN_ROLES), **{"domain_id": domain_id}
    )
    roles = {}
    for row in result:
        key = "d:%s" % row["id"]
        roles[key] = set(filter(None, row["roles"]))
        if row["parent_id"]:
            # Child domains inherit the roles of their parent
            parent_key = "d:{}".format(row["parent_id"])
            roles[key].update(roles[parent_key])
    # Convert the sets to lists so that they are JSON serialisable
    for k, v in roles.items():
        roles[k] = list(v)
    return DomainRoles(**{"domain_id": domain_id, "roles_map": roles})


def get_resource_permissions_for_roles(role_ids):  # noqa: E501
    """get_resource_permissions_for_roles

    Get a list of all resource permissions the specified roles have. # noqa: E501

    :param role_ids:
    :type role_ids: List[int]

    :rtype: List[ResourcePermission]
    """
    resource_permissions = db.session.get_bind().execute(text(SQL_RESOURCE_PERMISSIONS_FOR_ROLES),
                                                         role_ids=role_ids)
    return [ResourcePermission(**row) for row in resource_permissions]


def get_site_and_domain_roles(site_id):  # noqa: E501
    """get_site_and_domain_roles

    Get the site- and domain lineage roles defined for a given site. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteAndDomainRoles
    """
    site_rows = db.session.get_bind().execute(
        text(SQL_SITE_ROLES), **{"site_id": site_id}
    )
    roles = {}
    for site_row in site_rows:
        if site_row["domain_id"]:
            domain_rows = db.session.get_bind().execute(
                text(SQL_DOMAIN_ROLES), **{"domain_id": site_row["domain_id"]}
            )
            for row in domain_rows:
                key = "d:%s" % row["id"]
                roles[key] = set(filter(None, row["roles"]))
                if row["parent_id"]:
                    # Child domains inherit the roles of their parent
                    parent_key = "d:%s" % row["parent_id"]
                    roles[key].update(roles[parent_key])

        key = "s:%s" % site_row["id"]
        roles[key] = set(filter(None, site_row["roles"]))
        if site_row["domain_id"]:
            # Sites inherit the roles of their domain
            parent_key = "d:%s" % site_row["domain_id"]
            roles[key].update(roles[parent_key])

    for k, v in roles.items():
        roles[k] = list(v)

    return SiteAndDomainRoles(**{"roles_map": roles, "site_id": site_id})


def get_site_role_labels_aggregated(site_id):  # noqa: E501
    """get_site_role_labels_aggregated

    Get a list of all possible role labels that a user can have from the specified site&#39;s perspective. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteRoleLabelsAggregated
    """
    result = db.session.get_bind().execute(text(SQL_SITE_ROLE_LABELS_AGGREGATED), **{"site_id": site_id})
    return SiteRoleLabelsAggregated(
        **{"roles": [row["label"] for row in result],
        "site_id": site_id}
    )


def get_sites_under_domain(domain_id):  # noqa: E501
    """get_sites_under_domain

    Get a list of all sites linked directly or indirectly to the specified domain. # noqa: E501

    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: List[Site]
    """
    result = db.session.get_bind().execute(text(SQL_SITES_UNDER_DOMAIN), **{"domain_id": domain_id})
    return [Site(**row) for row in result]


def get_tech_admin_resource_permissions():  # noqa: E501
    """get_tech_admin_resource_permissions

    Get a list of all possible permissions any user can have. This is effectively what a tech admin user can do. # noqa: E501


    :rtype: List[ResourcePermission]
    """
    resource_permissions = db.session.get_bind().execute(text(SQL_TECH_ADMIN_RESOURCE_PERMISSIONS))
    return [ResourcePermission(**row) for row in resource_permissions]


def get_user_site_role_labels_aggregated(user_id, site_id):  # noqa: E501
    """get_user_site_role_labels_aggregated

    Get a list of all role labels that the specified user has from the specified site&#39;s perspective. # noqa: E501

    :param user_id: A UUID value identifying the user.
    :type user_id: dict | bytes
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: UserSiteRoleLabelsAggregated
    """
    sql = text(SQL_USER_SITE_ROLE_LABELS_AGGREGATED)
    result = db.session.get_bind().execute(sql, **{"user_id": user_id, "site_id": site_id})
    items = [row["label"] for row in result]
    obj = UserSiteRoleLabelsAggregated(
        **{"roles": items,
        "user_id": user_id,
        "site_id": site_id}
    )
    return obj


def get_users_with_roles_for_domain(domain_id):  # noqa: E501
    """get_users_with_roles_for_domain

    Get a list of Users with their effective roles within the given domain. # noqa: E501

    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: List[UserWithRoles]
    """
    sql = text(SQL_USERS_WITH_ROLES_FOR_DOMAIN)
    result = db.session.get_bind().execute(sql, **{"domain_id": domain_id})
    users_with_roles = [
        UserWithRoles(
            user_id=row["user_id"],
            role_ids=row["role_ids"]
        ) for row in result
    ]
    return users_with_roles


def get_users_with_roles_for_site(site_id):  # noqa: E501
    """get_users_with_roles_for_site

    Get a list of Users with their effective roles within the given site. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: List [UserWithRoles]
    """
    sql = text(SQL_USERS_WITH_ROLES_FOR_SITE)
    result = db.session.get_bind().execute(sql, **{"site_id": site_id})
    users_with_roles = [
        UserWithRoles(
            user_id=row["user_id"],
            role_ids=row["role_ids"]
        ) for row in result
    ]
    return users_with_roles


def healthcheck():  # noqa: E501
    """healthcheck

    Get the status of the service. # noqa: E501


    :rtype: HealthInfo
    """
    result = db.engine.execute("SELECT LOCALTIMESTAMP")
    db_timestamp = result.fetchone()[0]

    result = HealthInfo(
        host=socket.getfqdn(),
        server_timestamp=datetime.datetime.now(),
        version=__version__,
        db_timestamp=db_timestamp
    )
    return result

def purge_expired_invitations(cutoff_date=None):  # noqa: E501
    """purge_expired_invitations

    Purge all the expired invitations past a cutoff_date (defaults to today).

    :param cutoff_date: An optional cutoff date to purge invites before this date
    :type cutoff_date: str

    :rtype: PurgedInvitations
    """
    if cutoff_date is None:
        cutoff_date = str(datetime.datetime.now().date())

    # For some reason we have to do this SQL query in a transaction.
    # Ref: http://docs.sqlalchemy.org/en/latest/core/connections.html#using-transactions
    with db.session.get_bind().begin() as connection:
        result = connection.execute(
            text(SQL_PURGE_EXPIRED_INVITATIONS), **{"cutoff_date": cutoff_date}
        )

    amount = result.fetchone()["amount"]
    return PurgedInvitations(amount=amount)



