# coding: utf-8

from __future__ import absolute_import

import random
import uuid
import werkzeug

from flask import json

from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.domain_update import DomainUpdate  # noqa: E501
from swagger_server.test import BaseTestCase

from access_control import db_actions


class TestAccessControlRead(BaseTestCase):

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

    def test_domain_create(self):
        """Test case for domainrole_create
        """
        data = Domain(**{
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "Domain to create",
        })
        response = self.client.open(
            '/api/v1/domains',
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], data.name)
        self.assertEqual(r_data["description"], data.description)


    def test_domain_read(self):
        """Test case for domain_read
        """
        response = self.client.open(
            '/api/v1/domains/{domain_id}'.format(domain_id=self.domain_model.id),
            method='GET')
        r_data = json.loads(response.data)
        self.assertEqual(r_data["name"], self.domain_model.name)
        self.assertEqual(r_data["description"], self.domain_model.description)
        self.assertEqual(r_data["id"], self.domain_model.id)

    def test_domain_delete(self):
        """Test case for domain_delete
        """
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "Domain to delete",
        }
        model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=data,
            action="create"
        )
        response = self.client.open(
            '/api/v1/domains/{domain_id}'.format(domain_id=model.id),
            method='DELETE')

        with self.assertRaises(werkzeug.exceptions.NotFound):
            db_actions.crud(
                model="Domain",
                api_model=Domain,
                action="read",
                query={"id": model.id}
            )

    def test_domain_list(self):
        """Test case for domain_list
        """
        objects = []
        for index in range(1, random.randint(5, 20)):
            data = {
                "name": ("%s" % uuid.uuid1())[:30],
                "description": "Domain list %s" % index,
            }
            objects.append(db_actions.crud(
                model="Domain",
                api_model=Domain,
                data=data,
                action="create"
            ))
        query_string = [#('offset', 0),
                        ('domain_ids', ",".join(map(str, [domain.id for domain in objects])))]
        response = self.client.open(
            '/api/v1/domains',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), len(objects))
        query_string = [('limit', 2),
                        ('domain_ids', ",".join(map(str, [domain.id for domain in objects])))]
        response = self.client.open(
            '/api/v1/domains',
            method='GET',
            query_string=query_string)
        r_data = json.loads(response.data)
        self.assertEqual(len(r_data), 2)

    def test_domain_update(self):
        """Test case for domain_update
        """
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "Domain to update",
        }
        model = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=data,
            action="create"
        )
        data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "Domain updated",
        }
        data = DomainUpdate(
            **data
        )
        response = self.client.open(
            '/api/v1/domains/{domain_id}'.format(domain_id=model.id),
            method='PUT',
            data=json.dumps(data),
            content_type='application/json')
        r_data = json.loads(response.data)
        updated_entry = db_actions.crud(
            model="Domain",
            api_model=Domain,
            action="read",
            query={"id": model.id}
        )
        self.assertEqual(r_data["name"], updated_entry.name)
        self.assertEqual(r_data["description"], updated_entry.description)

    # TODO Ruan, Move out to seperate file like all the other tests.
    #def test_invitation_site_role_create(self):
    #    """Test case for invitationsiterole_create"""
    #    data = InvitationSiteRoleCreate(**{
    #        "invitation_id": self.invitation_model.id,
    #        "site_id": random.randint(2, 2000000),
    #        "role_id": random.randint(2, 2000000)
    #    })
    #    response = self.client.open(
    #        '/api/v1/invitationsiteroles',
    #        method='POST',
    #        data=json.dumps(data),
    #        content_type='application/json')
    #    r_data = json.loads(response.data)
    #    self.assertEqual(r_data["name"], data.name)
    #    self.assertEqual(r_data["description"], data.description)
