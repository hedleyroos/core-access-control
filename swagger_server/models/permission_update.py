# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PermissionUpdate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: str=None, description: str=None):  # noqa: E501
        """PermissionUpdate - a model defined in Swagger

        :param name: The name of this PermissionUpdate.  # noqa: E501
        :type name: str
        :param description: The description of this PermissionUpdate.  # noqa: E501
        :type description: str
        """
        self.swagger_types = {
            'name': str,
            'description': str
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description'
        }

        self._name = name
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'PermissionUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The permission_update of this PermissionUpdate.  # noqa: E501
        :rtype: PermissionUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this PermissionUpdate.


        :return: The name of this PermissionUpdate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this PermissionUpdate.


        :param name: The name of this PermissionUpdate.
        :type name: str
        """
        if name is not None and len(name) > 50:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `50`")  # noqa: E501

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this PermissionUpdate.


        :return: The description of this PermissionUpdate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this PermissionUpdate.


        :param description: The description of this PermissionUpdate.
        :type description: str
        """

        self._description = description
