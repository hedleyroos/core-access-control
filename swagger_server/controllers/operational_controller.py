import connexion
import six

from access_control.models import DB as db

from sqlalchemy import text

from swagger_server.models.all_user_roles import AllUserRoles  # noqa: E501
from swagger_server.models.domain_roles import DomainRoles  # noqa: E501
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles  # noqa: E501
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated  # noqa: E501
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated  # noqa: E501
from swagger_server import util


def get_all_user_roles(user_id):  # noqa: E501
    """get_all_user_roles

    Get the effective roles that a user has at any place in the organisational tree. # noqa: E501

    :param user_id: A UUID value identifying the user.
    :type user_id: dict | bytes

    :rtype: AllUserRoles
    """
    sql = text(
    """
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
    -- Return all the nodes of the tree with the implicit and explicit
    -- roles for the specified user. The domains are returned in breadth-first
    -- order. The list of roles needs to be post-processed as it may contain duplicates and NULL values, e.g.
    -- {6,null} or {null,null}
    SELECT id, parent_id, implicit_roles || explicit_roles AS roles
        FROM _roles;
    """
    )
    result = db.session.get_bind().execute(sql, **{"user_id": user_id})
    # {'roles_map': None, 'user_id': None}
    items = []
    for row in result:
        # (82, 73, [None, None])
        # TODO Nones need to be stripped.
        for item in row:
            items.append(item)
    return AllUserRoles(**{"roles_map": items, "user_id": user_id})


def get_domain_roles(domain_id):  # noqa: E501
    """get_domain_roles

    Get the domain and its lineage&#39;s roles defined for a domain. # noqa: E501

    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: DomainRoles
    """
    sql = text()
    result = db.session.get_bind().execute(sql)
    items = []
    for row in result:
        items.append(
            DomainRoles(**{})
        )
    return 'do some magic!'


def get_site_and_domain_roles(site_id):  # noqa: E501
    """get_site_and_domain_roles

    Get the site- and domain lineage roles defined for a given site. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteAndDomainRoles
    """
    sql = text()
    result = db.session.get_bind().execute(sql)
    items = []
    for row in result:
        items.append(
            SiteAndDomainRoles(**{})
        )
    return 'do some magic!'


def get_site_role_labels_aggregated(site_id):  # noqa: E501
    """get_site_role_labels_aggregated

    Get a list of all possible role labels that a user can have from the specified site&#39;s perspective. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteRoleLabelsAggregated
    """
    sql = text()
    result = db.session.get_bind().execute(sql)
    items = []
    for row in result:
        # ('<label_string>',)
        items.append(
            SiteRoleLabelsAggregated(
                **{"roles": [item for item in row],
                "site_id": site_id}
            )
        )
    return 'do some magic!'


def get_user_site_role_labels_aggregated(user_id, site_id):  # noqa: E501
    """get_user_site_role_labels_aggregated

    Get a list of all role labels that the specified user has from the specified site&#39;s perspective. # noqa: E501

    :param user_id: A UUID value identifying the user.
    :type user_id: dict | bytes
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: UserSiteRoleLabelsAggregated
    """
    sql = text(
    """
    -- Given a site id (:site_id) and a user id (:user_id), find all roles

    -- The recursive query needs to come first
    -- Get domain lineage ids
    WITH RECURSIVE _domain_lineage AS (
        SELECT domain.id, domain.parent_id
            FROM domain, site
        WHERE domain.id = site.domain_id
            AND site.client_id = :site_id
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
    )
    result = db.session.get_bind().execute(sql, **{"user_id": user_id, "site_id": site_id})
    items = []
    for row in result:
        # ('<label_string>',)
        for item in row:
            items.append(item)
    obj = UserSiteRoleLabelsAggregated(
        **{"roles": items,
        "user_id": user_id,
        "site_id": site_id}
    )
    return obj
