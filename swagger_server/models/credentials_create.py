# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class CredentialsCreate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, site_id: int=None, account_id: str=None, account_secret: str=None, description: str=None):  # noqa: E501
        """CredentialsCreate - a model defined in Swagger

        :param site_id: The site_id of this CredentialsCreate.  # noqa: E501
        :type site_id: int
        :param account_id: The account_id of this CredentialsCreate.  # noqa: E501
        :type account_id: str
        :param account_secret: The account_secret of this CredentialsCreate.  # noqa: E501
        :type account_secret: str
        :param description: The description of this CredentialsCreate.  # noqa: E501
        :type description: str
        """
        self.swagger_types = {
            'site_id': int,
            'account_id': str,
            'account_secret': str,
            'description': str
        }

        self.attribute_map = {
            'site_id': 'site_id',
            'account_id': 'account_id',
            'account_secret': 'account_secret',
            'description': 'description'
        }

        self._site_id = site_id
        self._account_id = account_id
        self._account_secret = account_secret
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'CredentialsCreate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The credentials_create of this CredentialsCreate.  # noqa: E501
        :rtype: CredentialsCreate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def site_id(self) -> int:
        """Gets the site_id of this CredentialsCreate.


        :return: The site_id of this CredentialsCreate.
        :rtype: int
        """
        return self._site_id

    @site_id.setter
    def site_id(self, site_id: int):
        """Sets the site_id of this CredentialsCreate.


        :param site_id: The site_id of this CredentialsCreate.
        :type site_id: int
        """
        if site_id is None:
            raise ValueError("Invalid value for `site_id`, must not be `None`")  # noqa: E501

        self._site_id = site_id

    @property
    def account_id(self) -> str:
        """Gets the account_id of this CredentialsCreate.


        :return: The account_id of this CredentialsCreate.
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id: str):
        """Sets the account_id of this CredentialsCreate.


        :param account_id: The account_id of this CredentialsCreate.
        :type account_id: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501
        if account_id is not None and len(account_id) > 256:
            raise ValueError("Invalid value for `account_id`, length must be less than or equal to `256`")  # noqa: E501
        if account_id is not None and len(account_id) < 32:
            raise ValueError("Invalid value for `account_id`, length must be greater than or equal to `32`")  # noqa: E501

        self._account_id = account_id

    @property
    def account_secret(self) -> str:
        """Gets the account_secret of this CredentialsCreate.


        :return: The account_secret of this CredentialsCreate.
        :rtype: str
        """
        return self._account_secret

    @account_secret.setter
    def account_secret(self, account_secret: str):
        """Sets the account_secret of this CredentialsCreate.


        :param account_secret: The account_secret of this CredentialsCreate.
        :type account_secret: str
        """
        if account_secret is None:
            raise ValueError("Invalid value for `account_secret`, must not be `None`")  # noqa: E501
        if account_secret is not None and len(account_secret) > 256:
            raise ValueError("Invalid value for `account_secret`, length must be less than or equal to `256`")  # noqa: E501
        if account_secret is not None and len(account_secret) < 32:
            raise ValueError("Invalid value for `account_secret`, length must be greater than or equal to `32`")  # noqa: E501

        self._account_secret = account_secret

    @property
    def description(self) -> str:
        """Gets the description of this CredentialsCreate.


        :return: The description of this CredentialsCreate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this CredentialsCreate.


        :param description: The description of this CredentialsCreate.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description