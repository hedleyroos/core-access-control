# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserWithRoles(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, user_id: str=None, role_ids: List[int]=None):  # noqa: E501
        """UserWithRoles - a model defined in Swagger

        :param user_id: The user_id of this UserWithRoles.  # noqa: E501
        :type user_id: str
        :param role_ids: The role_ids of this UserWithRoles.  # noqa: E501
        :type role_ids: List[int]
        """
        self.swagger_types = {
            'user_id': str,
            'role_ids': List[int]
        }

        self.attribute_map = {
            'user_id': 'user_id',
            'role_ids': 'role_ids'
        }

        self._user_id = user_id
        self._role_ids = role_ids

    @classmethod
    def from_dict(cls, dikt) -> 'UserWithRoles':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The user_with_roles of this UserWithRoles.  # noqa: E501
        :rtype: UserWithRoles
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this UserWithRoles.


        :return: The user_id of this UserWithRoles.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this UserWithRoles.


        :param user_id: The user_id of this UserWithRoles.
        :type user_id: str
        """

        self._user_id = user_id

    @property
    def role_ids(self) -> List[int]:
        """Gets the role_ids of this UserWithRoles.


        :return: The role_ids of this UserWithRoles.
        :rtype: List[int]
        """
        return self._role_ids

    @role_ids.setter
    def role_ids(self, role_ids: List[int]):
        """Sets the role_ids of this UserWithRoles.


        :param role_ids: The role_ids of this UserWithRoles.
        :type role_ids: List[int]
        """

        self._role_ids = role_ids