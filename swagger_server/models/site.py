# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class Site(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id: int=None, client_id: str=None, domain_id: int=None, name: str=None, description: str=None, created_at: datetime=None, updated_at: datetime=None):
        """
        Site - a model defined in Swagger

        :param id: The id of this Site.
        :type id: int
        :param client_id: The client_id of this Site.
        :type client_id: str
        :param domain_id: The domain_id of this Site.
        :type domain_id: int
        :param name: The name of this Site.
        :type name: str
        :param description: The description of this Site.
        :type description: str
        :param created_at: The created_at of this Site.
        :type created_at: datetime
        :param updated_at: The updated_at of this Site.
        :type updated_at: datetime
        """
        self.swagger_types = {
            'id': int,
            'client_id': str,
            'domain_id': int,
            'name': str,
            'description': str,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'client_id': 'client_id',
            'domain_id': 'domain_id',
            'name': 'name',
            'description': 'description',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }

        self._id = id
        self._client_id = client_id
        self._domain_id = domain_id
        self._name = name
        self._description = description
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'Site':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The site of this Site.
        :rtype: Site
        """
        return deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """
        Gets the id of this Site.

        :return: The id of this Site.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """
        Sets the id of this Site.

        :param id: The id of this Site.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def client_id(self) -> str:
        """
        Gets the client_id of this Site.

        :return: The client_id of this Site.
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id: str):
        """
        Sets the client_id of this Site.

        :param client_id: The client_id of this Site.
        :type client_id: str
        """

        self._client_id = client_id

    @property
    def domain_id(self) -> int:
        """
        Gets the domain_id of this Site.

        :return: The domain_id of this Site.
        :rtype: int
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id: int):
        """
        Sets the domain_id of this Site.

        :param domain_id: The domain_id of this Site.
        :type domain_id: int
        """
        if domain_id is None:
            raise ValueError("Invalid value for `domain_id`, must not be `None`")

        self._domain_id = domain_id

    @property
    def name(self) -> str:
        """
        Gets the name of this Site.

        :return: The name of this Site.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name of this Site.

        :param name: The name of this Site.
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
        Gets the description of this Site.

        :return: The description of this Site.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """
        Sets the description of this Site.

        :param description: The description of this Site.
        :type description: str
        """

        self._description = description

    @property
    def created_at(self) -> datetime:
        """
        Gets the created_at of this Site.

        :return: The created_at of this Site.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """
        Sets the created_at of this Site.

        :param created_at: The created_at of this Site.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """
        Gets the updated_at of this Site.

        :return: The updated_at of this Site.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """
        Sets the updated_at of this Site.

        :param updated_at: The updated_at of this Site.
        :type updated_at: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")

        self._updated_at = updated_at
