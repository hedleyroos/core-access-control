# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserResourceRole(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, user_id: str=None, resource_id: int=None, role_id: int=None, created_at: datetime=None, updated_at: datetime=None):  # noqa: E501
        """UserResourceRole - a model defined in Swagger

        :param user_id: The user_id of this UserResourceRole.  # noqa: E501
        :type user_id: str
        :param resource_id: The resource_id of this UserResourceRole.  # noqa: E501
        :type resource_id: int
        :param role_id: The role_id of this UserResourceRole.  # noqa: E501
        :type role_id: int
        :param created_at: The created_at of this UserResourceRole.  # noqa: E501
        :type created_at: datetime
        :param updated_at: The updated_at of this UserResourceRole.  # noqa: E501
        :type updated_at: datetime
        """
        self.swagger_types = {
            'user_id': str,
            'resource_id': int,
            'role_id': int,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'user_id': 'user_id',
            'resource_id': 'resource_id',
            'role_id': 'role_id',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }

        self._user_id = user_id
        self._resource_id = resource_id
        self._role_id = role_id
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'UserResourceRole':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The user_resource_role of this UserResourceRole.  # noqa: E501
        :rtype: UserResourceRole
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this UserResourceRole.


        :return: The user_id of this UserResourceRole.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this UserResourceRole.


        :param user_id: The user_id of this UserResourceRole.
        :type user_id: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def resource_id(self) -> int:
        """Gets the resource_id of this UserResourceRole.


        :return: The resource_id of this UserResourceRole.
        :rtype: int
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id: int):
        """Sets the resource_id of this UserResourceRole.


        :param resource_id: The resource_id of this UserResourceRole.
        :type resource_id: int
        """
        if resource_id is None:
            raise ValueError("Invalid value for `resource_id`, must not be `None`")  # noqa: E501

        self._resource_id = resource_id

    @property
    def role_id(self) -> int:
        """Gets the role_id of this UserResourceRole.


        :return: The role_id of this UserResourceRole.
        :rtype: int
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id: int):
        """Sets the role_id of this UserResourceRole.


        :param role_id: The role_id of this UserResourceRole.
        :type role_id: int
        """
        if role_id is None:
            raise ValueError("Invalid value for `role_id`, must not be `None`")  # noqa: E501

        self._role_id = role_id

    @property
    def created_at(self) -> datetime:
        """Gets the created_at of this UserResourceRole.


        :return: The created_at of this UserResourceRole.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """Sets the created_at of this UserResourceRole.


        :param created_at: The created_at of this UserResourceRole.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """Gets the updated_at of this UserResourceRole.


        :return: The updated_at of this UserResourceRole.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """Sets the updated_at of this UserResourceRole.


        :param updated_at: The updated_at of this UserResourcResource
        :type updated_at: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at
