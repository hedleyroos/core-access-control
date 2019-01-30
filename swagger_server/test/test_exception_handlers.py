# coding: utf-8

from __future__ import absolute_import

import uuid

import psycopg2
from flask import json
from ge_core_shared import db_actions, decorators
from sqlalchemy.orm.exc import StaleDataError

from swagger_server.models.domain import Domain
from swagger_server.test import BaseTestCase
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

from project.settings import API_KEY_HEADER


class TestExceptions(BaseTestCase):

    @decorators.db_exception
    def setUp(self):
        super().setUp()
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

        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_response(self):
        data = Domain(**self.domain_data)
        response = self.client.open(
            '/api/v1/domains',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            r_data["error"],
            "ERROR:  duplicate key value violates unique " \
            "constraint \"ix_domain_name\" "\
            "DETAIL:  "\
            "Key (name)=(%s) already exists." % self.domain_model.name
        )

    @patch("ge_core_shared.db_actions.db.session.commit")
    def test_operationalerror_response(self, mocked_crud):
        error = SQLAlchemyError(
            "Server closed the connection unexpectedly"
        )
        error.orig = psycopg2.OperationalError("Server closed the connection unexpectedly")
        mocked_crud.side_effect = error
        data = Domain(**{
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test domain",
        })
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
            "OperationalError('Server closed the connection unexpectedly',)"
        )

    @patch("ge_core_shared.db_actions.db.session.commit")
    def test_staledataerror_response(self, mocked_crud):

        error = StaleDataError("Some reason")
        mocked_crud.side_effect = error
        data = Domain(**{
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "a super cool test domain",
        })
        response = self.client.open(
            '/api/v1/domains',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers)
        r_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            "StaleDataError(Some reason)",
            r_data["error"]
        )
