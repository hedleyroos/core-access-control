# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class Resource(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id: int=None, urn: str=None, description: str=None, created_at: datetime=None, updated_at: datetime=None):
        """
        Resource - a model defined in Swagger

        :param id: The id of this Resource.
        :type id: int
        :param urn: The urn of this Resource.
        :type urn: str
        :param description: The description of this Resource.
        :type description: str
        :param created_at: The created_at of this Resource.
        :type created_at: datetime
        :param updated_at: The updated_at of this Resource.
        :type updated_at: datetime
        """
        self.swagger_types = {
            'id': int,
            'urn': str,
            'description': str,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'urn': 'urn',
            'description': 'description',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }

        self._id = id
        self._urn = urn
        self._description = description
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'Resource':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The resource of this Resource.
        :rtype: Resource
        """
        return deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """
        Gets the id of this Resource.

        :return: The id of this Resource.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """
        Sets the id of this Resource.

        :param id: The id of this Resource.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def urn(self) -> str:
        """
        Gets the urn of this Resource.

        :return: The urn of this Resource.
        :rtype: str
        """
        return self._urn

    @urn.setter
    def urn(self, urn: str):
        """
        Sets the urn of this Resource.

        :param urn: The urn of this Resource.
        :type urn: str
        """
        if urn is None:
            raise ValueError("Invalid value for `urn`, must not be `None`")

        self._urn = urn

    @property
    def description(self) -> str:
        """
        Gets the description of this Resource.

        :return: The description of this Resource.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """
        Sets the description of this Resource.

        :param description: The description of this Resource.
        :type description: str
        """

        self._description = description

    @property
    def created_at(self) -> datetime:
        """
        Gets the created_at of this Resource.

        :return: The created_at of this Resource.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """
        Sets the created_at of this Resource.

        :param created_at: The created_at of this Resource.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """
        Gets the updated_at of this Resource.

        :return: The updated_at of this Resource.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """
        Sets the updated_at of this Resource.

        :param updated_at: The updated_at of this Resource.
        :type updated_at: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")

        self._updated_at = updated_at

