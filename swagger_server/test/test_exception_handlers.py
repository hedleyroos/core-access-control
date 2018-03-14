# coding: utf-8

from __future__ import absolute_import

import random
import uuid

import os
import werkzeug

from flask import json

from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.domain_update import DomainUpdate  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import db_actions


class TestExceptions(BaseTestCase):

    def setUp(self):
        self.domain_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test domain",
        }
        self.domain_model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.domain_data,
            action="create"
        )

        # Test env settings
        os.environ["ALLOWED_API_KEYS"] = "ahjaeK1thee9aixuogho"

        self.headers = {"X-API-KEY": "ahjaeK1thee9aixuogho"}

    def test_response(self):
        data = Domain(**self.domain_data)
        response = self.client.open(
            '/api/v1/domains',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            r_data["error"],
            "(psycopg2.IntegrityError) duplicate key value violates unique " \
            "constraint \"ix_domain_name\" "\
            "DETAIL:  "\
            "Key (name)=(%s) already exists. " % self.domain_model.name
        )

