# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class Invitation(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id: str=None, invitor_id: str=None, first_name: str=None, last_name: str=None, email: str=None, expires_at: datetime=None, created_at: datetime=None, updated_at: datetime=None):
        """
        Invitation - a model defined in Swagger

        :param id: The id of this Invitation.
        :type id: str
        :param invitor_id: The invitor_id of this Invitation.
        :type invitor_id: str
        :param first_name: The first_name of this Invitation.
        :type first_name: str
        :param last_name: The last_name of this Invitation.
        :type last_name: str
        :param email: The email of this Invitation.
        :type email: str
        :param expires_at: The expires_at of this Invitation.
        :type expires_at: datetime
        :param created_at: The created_at of this Invitation.
        :type created_at: datetime
        :param updated_at: The updated_at of this Invitation.
        :type updated_at: datetime
        """
        self.swagger_types = {
            'id': str,
            'invitor_id': str,
            'first_name': str,
            'last_name': str,
            'email': str,
            'expires_at': datetime,
            'created_at': datetime,
            'updated_at': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'invitor_id': 'invitor_id',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'expires_at': 'expires_at',
            'created_at': 'created_at',
            'updated_at': 'updated_at'
        }

        self._id = id
        self._invitor_id = invitor_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._expires_at = expires_at
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'Invitation':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The invitation of this Invitation.
        :rtype: Invitation
        """
        return deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """
        Gets the id of this Invitation.

        :return: The id of this Invitation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """
        Sets the id of this Invitation.

        :param id: The id of this Invitation.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def invitor_id(self) -> str:
        """
        Gets the invitor_id of this Invitation.
        The user that created the invitation

        :return: The invitor_id of this Invitation.
        :rtype: str
        """
        return self._invitor_id

    @invitor_id.setter
    def invitor_id(self, invitor_id: str):
        """
        Sets the invitor_id of this Invitation.
        The user that created the invitation

        :param invitor_id: The invitor_id of this Invitation.
        :type invitor_id: str
        """
        if invitor_id is None:
            raise ValueError("Invalid value for `invitor_id`, must not be `None`")

        self._invitor_id = invitor_id

    @property
    def first_name(self) -> str:
        """
        Gets the first_name of this Invitation.

        :return: The first_name of this Invitation.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """
        Sets the first_name of this Invitation.

        :param first_name: The first_name of this Invitation.
        :type first_name: str
        """
        if first_name is None:
            raise ValueError("Invalid value for `first_name`, must not be `None`")
        if first_name is not None and len(first_name) > 100:
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `100`")

        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """
        Gets the last_name of this Invitation.

        :return: The last_name of this Invitation.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """
        Sets the last_name of this Invitation.

        :param last_name: The last_name of this Invitation.
        :type last_name: str
        """
        if last_name is None:
            raise ValueError("Invalid value for `last_name`, must not be `None`")
        if last_name is not None and len(last_name) > 100:
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `100`")

        self._last_name = last_name

    @property
    def email(self) -> str:
        """
        Gets the email of this Invitation.

        :return: The email of this Invitation.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """
        Sets the email of this Invitation.

        :param email: The email of this Invitation.
        :type email: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")

        self._email = email

    @property
    def expires_at(self) -> datetime:
        """
        Gets the expires_at of this Invitation.

        :return: The expires_at of this Invitation.
        :rtype: datetime
        """
        return self._expires_at

    @expires_at.setter
    def expires_at(self, expires_at: datetime):
        """
        Sets the expires_at of this Invitation.

        :param expires_at: The expires_at of this Invitation.
        :type expires_at: datetime
        """
        if expires_at is None:
            raise ValueError("Invalid value for `expires_at`, must not be `None`")

        self._expires_at = expires_at

    @property
    def created_at(self) -> datetime:
        """
        Gets the created_at of this Invitation.

        :return: The created_at of this Invitation.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """
        Sets the created_at of this Invitation.

        :param created_at: The created_at of this Invitation.
        :type created_at: datetime
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def updated_at(self) -> datetime:
        """
        Gets the updated_at of this Invitation.

        :return: The updated_at of this Invitation.
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """
        Sets the updated_at of this Invitation.

        :param updated_at: The updated_at of this Invitation.
        :type updated_at: datetime
        """
        if updated_at is None:
            raise ValueError("Invalid value for `updated_at`, must not be `None`")

        self._updated_at = updated_at
