import connexion
from swagger_server.models.all_user_roles import AllUserRoles
from swagger_server.models.domain_roles import DomainRoles
from swagger_server.models.site_and_domain_roles import SiteAndDomainRoles
from swagger_server.models.site_role_labels_aggregated import SiteRoleLabelsAggregated
from swagger_server.models.user_site_role_labels_aggregated import UserSiteRoleLabelsAggregated
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def get_all_user_roles(user_id):
    """
    get_all_user_roles
    Get the effective roles that a user has at any place in the organisational tree.
    :param user_id: A UUID value identifying the user.
    :type user_id: str

    :rtype: AllUserRoles
    """
    return 'do some magic!'


def get_domain_roles(domain_id):
    """
    get_domain_roles
    Get the domain and its lineage&#39;s roles defined for a domain.
    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: DomainRoles
    """
    return 'do some magic!'


def get_site_and_domain_roles(site_id):
    """
    get_site_and_domain_roles
    Get the site- and domain lineage roles defined for a given site.
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteAndDomainRoles
    """
    return 'do some magic!'


def get_site_role_labels_aggregated(site_id):
    """
    get_site_role_labels_aggregated
    Get a list of all possible role labels that a user can have from the specified site&#39;s perspective.
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteRoleLabelsAggregated
    """
    return 'do some magic!'


def get_user_site_role_labels_aggregated(user_id, site_id):
    """
    get_user_site_role_labels_aggregated
    Get a list of all role labels that the specified user has from the specified site&#39;s perspective.
    :param user_id: A UUID value identifying the user.
    :type user_id: str
    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: UserSiteRoleLabelsAggregated
    """
    return 'do some magic!'
