import six

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
    return 'do some magic!'


def get_domain_roles(domain_id):  # noqa: E501
    """get_domain_roles

    Get the domain and its lineage&#39;s roles defined for a domain. # noqa: E501

    :param domain_id: A unique integer value identifying the domain.
    :type domain_id: int

    :rtype: DomainRoles
    """
    return 'do some magic!'


def get_site_and_domain_roles(site_id):  # noqa: E501
    """get_site_and_domain_roles

    Get the site- and domain lineage roles defined for a given site. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteAndDomainRoles
    """
    return 'do some magic!'


def get_site_role_labels_aggregated(site_id):  # noqa: E501
    """get_site_role_labels_aggregated

    Get a list of all possible role labels that a user can have from the specified site&#39;s perspective. # noqa: E501

    :param site_id: A unique integer value identifying the site.
    :type site_id: int

    :rtype: SiteRoleLabelsAggregated
    """
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
    return 'do some magic!'
