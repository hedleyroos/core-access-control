from unittest import TestCase
import jsonschema
import uuid

from ge_core_shared.db_actions import crud

from access_control import models
from access_control.fixtures.deletionmethods import DELETION_METHODS
from project.app import DB as db
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501
from swagger_server.models.site_create import SiteCreate  # noqa: E501


class SiteModelValidationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create the DeletionMethods.
        cls.method_one = models.DeletionMethod(**{
            "label": "email_test",
            "data_schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "recipients": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "email"
                        }
                    },
                },
            },
            "description": "A description"
        })
        db.session.add(cls.method_one)
        db.session.commit()
        domain_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "description": "%s" % uuid.uuid1(),
        }
        cls.domain_model = crud(
            model="Domain",
            api_model=Domain,
            data=domain_data,
            action="create"
        )

    def test_deletion_method_data_validation(self):
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": self.method_one.id,
            "deletion_method_data": {"en": "a"},
            "client_id": 9994,
            "is_active": True,
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": self.method_one.id,
            "deletion_method_data": {"recipients": ['A@a.com', 'B@b.com']},
            "client_id": 9995,
            "is_active": True,
        }
        crud(
            model="Site",
            api_model=SiteCreate,
            data=site_data,
            action="create"
        )

    def test_fixture_schema_validation(self):
        none_method = models.DeletionMethod.query.filter_by(id=0).first_or_404()
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": none_method.id,
            "deletion_method_data": {"a": "a"},
            "client_id": 9996,
            "is_active": True,
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": none_method.id,
            "deletion_method_data": {},
            "client_id": 9994,
            "is_active": True,
        }
        crud(
            model="Site",
            api_model=SiteCreate,
            data=site_data,
            action="create"
        )

        email_method = models.DeletionMethod(**DELETION_METHODS[0])
        db.session.add(email_method)
        db.session.commit()
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": email_method.id,
            "deletion_method_data": {"a": "a"},
            "client_id": 9996,
            "is_active": True,
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": email_method.id,
            "deletion_method_data": {"recipients": ['A@a.com', 'B@b.com']},
            "client_id": 9997,
            "is_active": True,
        }
        crud(
            model="Site",
            api_model=SiteCreate,
            data=site_data,
            action="create"
        )

        api_method = models.DeletionMethod(**DELETION_METHODS[1])
        db.session.add(api_method)
        db.session.commit()
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": api_method.id,
            "deletion_method_data": {"a": "a"},
            "client_id": 9998,
            "is_active": True,
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            crud(
                model="Site",
                api_model=Site,
                data=site_data,
                action="create"
            )
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": api_method.id,
            "deletion_method_data": {"body": {"user_id": str(uuid.uuid1())}},
            "client_id": 9999,
            "is_active": True,
        }
        crud(
            model="Site",
            api_model=SiteCreate,
            data=site_data,
            action="create"
        )
