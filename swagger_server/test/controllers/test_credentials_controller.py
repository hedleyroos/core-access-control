# coding: utf-8

from __future__ import absolute_import

import random
import uuid

import werkzeug
from flask import json

from project.settings import API_KEY_HEADER
from ge_core_shared import db_actions, decorators

from swagger_server.models import CredentialsCreate, Site, Domain, SiteCreate
from swagger_server.models.credentials import Credentials  # noqa: E501
from swagger_server.models.credentials_update import CredentialsUpdate  # noqa: E501
from swagger_server.test import BaseTestCase, db_create_entry


class CredentialsTestCase(BaseTestCase):

    @decorators.db_exception
    def setUp(self):
        super().setUp()
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data={
                "name": "TestDomain",
                "description": "A test domain"
            },
            action="create"
        )
        self.site_model = db_create_entry(
            model="Site",
            data={
                "name": "TestSite",
                "domain_id": self.domain_model.id,
                "description": "A test site",
            },
        )
        self.credentials_data = {
            "site_id": self.site_model.id,
            "account_id": "accountid".rjust(32, "0"),
            "account_secret": "accountsecret".rjust(32, "0"),
            "description": "Super cool test credentials",
        }
        self.credentials_model = db_actions.crud(
            model="Credentials",
            api_model=Credentials,
            data=self.credentials_data,
            action="create"
        )

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_credentials_create(self):
        """Test case for credentials_create
        """
        data = CredentialsCreate(**{
            "site_id": self.site_model.id,
            "account_id": "anaccountid".rjust(32, "0"),
            "account_secret": "anaccountsecret".rjust(32, "0"),
            "description": "Super cool test credentials",
        })
        response = self.client.open(
            '/api/v1/credentials',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["site_id"], data.site_id)
        self.assertEqual(r_data["account_id"], data.account_id)
        self.assertEqual(r_data["account_secret"], data.account_secret)
        self.assertEqual(r_data["description"], data.description)

    def test_credentials_read(self):
        """Test case for credentials_read
        """
        response = self.client.open(
            '/api/v1/credentials/{credentials_id}'.format(credentials_id=self.credentials_model.id),
            method='GET', headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(r_data["id"], self.credentials_model.id)
        self.assertEqual(r_data["site_id"], self.credentials_model.site_id)
        self.assertEqual(r_data["account_id"], self.credentials_model.account_id)
        self.assertEqual(r_data["account_secret"], self.credentials_model.account_secret)
        self.assertEqual(r_data["description"], self.credentials_model.description)

    def test_credentials_delete(self):
        """Test case for credentials_delete
        """
        data = {
            "site_id": self.site_model.id,
            "account_id": "accountid2".rjust(32, "0"),
            "account_secret": "accountsecret2".rjust(32, "0"),
            "description": "Super cool test credentials 2",
        }
        model = db_actions.crud(
            model="Credentials",
            api_model=Credentials,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/credentials/{credentials_id}'.format(credentials_id=model.id),
            method='DELETE', headers=self.headers)

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                action="read",
                query={"id": model.id}
            )

    def test_credentials_list(self):
        """Test case for credentials_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "site_id": self.site_model.id,
                "account_id": f"accountid {index}".rjust(32, "0"),
                "account_secret": f"accountsecret {index}".rjust(32, "0"),
                "description": f"Super cool test credentials {index}",
            }
            objects.append(db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('credentials_ids', ",".join(map(str, [credentials.id for credentials in objects])))]
        response = self.client.open(
            '/api/v1/credentials',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))
        query_string = [('limit', 2),
                        ('credentials_ids', ",".join(map(str, [credentials.id for credentials in objects])))]
        response = self.client.open(
            '/api/v1/credentials',
            method='GET',
            query_string=query_string,
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)
        self.assertEqual(int(response.headers["X-Total-Count"]), len(objects))

    def test_credentials_update(self):
        """Test case for credentials_update
        """
        data = {
            "site_id": self.site_model.id,
            "account_id": "oldaccountid".rjust(32, "0"),
            "account_secret": "oldaccountsecret".rjust(32, "0"),
            "description": "Old super cool test credentials",
        }
        model = db_actions.crud(
            model="Credentials",
            api_model=Credentials,
            data=data,
            action="create"
        )
        data = {
            "site_id": self.site_model.id,
            "account_id": "newaccountid".rjust(32, "0"),
            "account_secret": "newaccountsecret".rjust(32, "0"),
            "description": "New super cool test credentials",
        }
        data = CredentialsUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/credentials/{credentials_id}'.format(credentials_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Credentials",
            api_model=Credentials,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["site_id"], updated_entry.site_id)
        self.assertEqual(r_data["account_id"], updated_entry.account_id)
        self.assertEqual(r_data["account_secret"], updated_entry.account_secret)
        self.assertEqual(r_data["description"], updated_entry.description)

    def test_credentials_length(self):
        # account_id too short
        with self.assertRaises(ValueError):
            db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                action="create",
                data={
                    "site_id": self.site_model.id,
                    "account_id": "0000",
                    "account_secret": "".rjust(32),
                    "description": "A test"
                }
            )

        # account_secret too short
        with self.assertRaises(ValueError):
            db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                action="create",
                data={
                    "site_id": self.site_model.id,
                    "account_id": "".rjust(32),
                    "account_secret": "000",
                    "description": "A test"
                }
            )

        # No error
        db_actions.crud(
            model="Credentials",
            api_model=Credentials,
            action="create",
            data={
                "site_id": self.site_model.id,
                "account_id": "123".rjust(32),
                "account_secret": "123".rjust(32),
                "description": "A test"
            }
        )

        # account_id too long
        with self.assertRaises(ValueError):
            db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                action="create",
                data={
                    "site_id": self.site_model.id,
                    "account_id": "".rjust(257),
                    "account_secret": "".rjust(32),
                    "description": "A test"
                }
            )

        # account_secret too long
        with self.assertRaises(ValueError):
            db_actions.crud(
                model="Credentials",
                api_model=Credentials,
                action="create",
                data={
                    "site_id": self.site_model.id,
                    "account_id": "".rjust(32),
                    "account_secret": "".rjust(257),
                    "description": "A test"
                }
            )

