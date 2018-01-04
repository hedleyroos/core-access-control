# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class Domain(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id: int=None, parent_id: int=None, name: str=None, description: str=None, created_at: datetime=None, updated_at: datetime=None):
        """
        Domain - a model defined in Swagger

        :param id: The id of this Domain.
        :type id: int
        :param parent_id: The parent_id of this Domain.
        :type parent_id: int
        :param name: The name of this Domain.
        :type name: str
        :param description: The description of this Domain.
        :type description: str
        :param created_at: The created_at of this Domain.
        :type created_at: datetime
        :param updated_at: The updated_at of this Domain.
        :type updated_at: datetime
        """
        self.swagger_types = {
            'id': int,
            'parent_id': int,
            'name': str,
            'description': str,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'parent_id': 'parent_id',
            'name': 'name',
            'description': 'description',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }

        self._id = id
        self._parent_id = parent_id
        self._name = name
        self._description = description
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'Domain':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The domain of this Domain.
        :rtype: Domain
        """
        return deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """
        Gets the id of this Domain.

        :return: The id of this Domain.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """
        Sets the id of this Domain.

        :param id: The id of this Domain.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def parent_id(self) -> int:
        """
        Gets the parent_id of this Domain.

        :return: The parent_id of this Domain.
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id: int):
        """
        Sets the parent_id of this Domain.

        :param parent_id: The parent_id of this Domain.
        :type parent_id: int
        """

        self._parent_id = parent_id

    @property
    def name(self) -> str:
        """
        Gets the name of this Domain.

        :return: The name of this Domain.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name of this Domain.

        :param name: The name of this Domain.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if name is not None and len(name) > 100:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `100`")

        self._name = name

    @property
    def description(self) -> str:
        """
        Gets the description of this Domain.

        :return: The description of this Domain.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """
        Sets the description of this Domain.

        :param description: The description of this Domain.
        :type description: str
        """

        self._description = description

    @property
    def created_at(self) -> datetime:
        """
        Gets the created_at of this Domain.

        :return: The created_at of this Domain.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """
        Sets the created_at of this Domain.

        :param created_at: The created_at of this Domain.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """
        Gets the updated_at of this Domain.

        :return: The updated_at of this Domain.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """
        Sets the updated_at of this Domain.

        :param updated_at: The updated_at of this Domain.
        :type updated_at: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")

        self._updated_at = updated_at

