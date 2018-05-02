import connexion
import six

import project.app

from sqlalchemy import text

from swagger_server.models.all_user_roles import AllUserRoles  # noqa: E501
from swagger_server.models.domain_roles import DomainRoles  # noqa: E501
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles  # noqa: E501
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_and_roles import UserAndRoles
from swagger_server import util

db = project.app.DB

SQL_ALL_DOMAIN_ROLES_FOR_USER = """
-- Given a user id (:user_id), find all roles in the organisational domain tree

-- Finding all the implicit and explicit roles is simple,
-- however, we need to return the results in such a way
-- that the domain hierarchy can be interpreted and roles
-- pushed down the tree.

WITH RECURSIVE _domain_tree AS (
  SELECT domain.id, domain.parent_id, 0 AS position
    FROM domain AS domain
   WHERE domain.parent_id IS NULL  -- The root domain
   UNION
  SELECT domain.id, domain.parent_id,
         _domain_tree.position + 1 AS position
    FROM _domain_tree,
         domain AS domain
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

SQL_ALL_SITE_ROLES_FOR_USER = """
WITH _roles AS (
  SELECT site.id, site.domain_id,
         -- Site roles are distinct per definition
         array_agg(siterole.role_id) AS implicit_roles,
         -- User site roles are distinct per definition
         array_agg(usersiterole.role_id) AS explicit_roles
    FROM site AS site
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
    FROM domain AS domain
   WHERE domain.id = :domain_id
   UNION
  SELECT domain.id, domain.parent_id,
         _domain_tree.position - 1 AS position
    FROM _domain_tree,
         domain AS domain
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
FROM site AS site
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
-- Given the domain_id, find all roles each user has on that domain.

-- We find all the domains above the given domain in the hierarchy
-- in order to find all effective roles the a user has.
WITH RECURSIVE _parent_domains AS (
  SELECT domain.id, domain.parent_id, domain.name
    FROM domain AS domain
   WHERE domain.id = :domain_id
   UNION
  SELECT domain.id, domain.parent_id, domain.name
    FROM _parent_domains,
         domain AS domain
   WHERE domain.id = _parent_domains.parent_id
),
_roles AS (
  SELECT userdomainrole.user_id,
         -- User domain roles are distinct per definition
         array_agg(DISTINCT userdomainrole.role_id) AS effective_roles
    FROM _parent_domains AS domain
    LEFT OUTER JOIN user_domain_role AS userdomainrole
         ON (domain.id = userdomainrole.domain_id)
   WHERE userdomainrole.user_id IS NOT NULL
   GROUP BY userdomainrole.user_id
)
-- Return all the roles per user for the domain. The list of roles needs to be post-processed
-- as it may contain duplicates and NULL values, e.g. {6,null} or {null,null}
SELECT user_id, effective_roles AS role_ids
  FROM _roles;
"""

SQL_USERS_WITH_ROLES_FOR_SITE = """
-- Given the site_id, find all roles each user has on that site.

-- Simply get all roles on the usersiteroles and group by user_id.
-- Also all explicit site roles are included.
WITH RECURSIVE _parent_domains AS (
  SELECT domain.id, domain.parent_id, domain.name
  FROM domain AS domain,
       (
         SELECT site.id, site.domain_id
          FROM site as site
         WHERE site.id = :site_id
         LIMIT 1
       ) as site
  WHERE domain.id = site.domain_id
  UNION
  SELECT domain.id, domain.parent_id, domain.name
  FROM _parent_domains,
       domain AS domain
  WHERE domain.id = _parent_domains.parent_id
),
_roles AS (
  SELECT userdomainrole.user_id AS user_id,
         -- User domain roles are distinct per definition
         userdomainrole.role_id AS role_id
    FROM _parent_domains as domain
   LEFT OUTER JOIN user_domain_role AS userdomainrole
        ON (userdomainrole.domain_id = domain.id)
   WHERE userdomainrole.user_id IS NOT NULL
  UNION ALL
  SELECT usersiterole.user_id AS user_id,
         -- User site roles are distinct per definition
         usersiterole.role_id AS role_id
    FROM user_site_role AS usersiterole
   WHERE usersiterole.user_id IS NOT NULL
)

-- Return all roles per user for the site. The list of roles needs to be post-processed
-- as it may contain duplicates and NULL values, e.g. {6,null} or {null,null}
SELECT user_id, array_agg(DISTINCT role_id) as role_ids
  FROM _roles
GROUP BY user_id;
"""


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


def get_users_with_roles_for_domain(domain_id): # noqa: E501
    """get_users_with_roles_for_domain

    Get a list of all users with their roles on a given domain.

    :param domain_id: An ID of a domain.
    :type domain_id: int

    :rtype: UserAndRoles
    """
    sql = text(SQL_USERS_WITH_ROLES_FOR_DOMAIN)
    result = db.session.get_bind().execute(sql, **{"domain_id": domain_id})
    users_and_roles = [
        UserAndRoles(**{
            "user_id": row["user_id"], 
            "role_ids": row["role_ids"]
        }) for row in result
    ]
    return users_and_roles


def get_users_with_roles_for_site(site_id): # noqa: E501
    """get_users_with_roles_for_site

    Get a list of all users with their roles on a given site.

    :param site_id: An ID of a domain.
    :type site_id: int

    :rtype: UserAndRoles
    """
    sql = text(SQL_USERS_WITH_ROLES_FOR_SITE)
    result = db.session.get_bind().execute(sql, **{"site_id": site_id})
    users_and_roles = [
        UserAndRoles(**{
            "user_id": row["user_id"],
            "role_ids": row["role_ids"]
        }) for row in result
    ]
    return users_and_roles
