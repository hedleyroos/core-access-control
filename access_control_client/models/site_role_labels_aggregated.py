# coding: utf-8

"""
    Access Control API

    # The Access Control API  ## Overview The Access Control API is an API exposed to other core components. It uses an API Key in an HTTP header to perform authentication and authorisation.  Most of the API calls facilitates CRUD of the entities defined in the Access Control component. Others calls allows the retrieval of information in a form that is convenient for other components (most notably the Management Layer) to consume. 

    OpenAPI spec version: 
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SiteRoleLabelsAggregated(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'site_id': 'int',
        'roles': 'list[RoleLabel]'
    }

    attribute_map = {
        'site_id': 'site_id',
        'roles': 'roles'
    }

    def __init__(self, site_id=None, roles=None):
        """
        SiteRoleLabelsAggregated - a model defined in Swagger
        """

        self._site_id = None
        self._roles = None

        if site_id is not None:
          self.site_id = site_id
        if roles is not None:
          self.roles = roles

    @property
    def site_id(self):
        """
        Gets the site_id of this SiteRoleLabelsAggregated.

        :return: The site_id of this SiteRoleLabelsAggregated.
        :rtype: int
        """
        return self._site_id

    @site_id.setter
    def site_id(self, site_id):
        """
        Sets the site_id of this SiteRoleLabelsAggregated.

        :param site_id: The site_id of this SiteRoleLabelsAggregated.
        :type: int
        """

        self._site_id = site_id

    @property
    def roles(self):
        """
        Gets the roles of this SiteRoleLabelsAggregated.

        :return: The roles of this SiteRoleLabelsAggregated.
        :rtype: list[RoleLabel]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """
        Sets the roles of this SiteRoleLabelsAggregated.

        :param roles: The roles of this SiteRoleLabelsAggregated.
        :type: list[RoleLabel]
        """

        self._roles = roles

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, SiteRoleLabelsAggregated):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
