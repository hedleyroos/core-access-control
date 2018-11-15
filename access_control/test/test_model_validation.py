from unittest import TestCase
import jsonschema
import uuid

from ge_core_shared.db_actions import get_or_create, delete_entry, list_entry, crud

from access_control import models
from project.app import DB as db
from swagger_server.models.domain import Domain  # noqa: E501
from swagger_server.models.site import Site  # noqa: E501


class ListFiltersTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create the DeletionMethods.
        cls.method_one = models.DeletionMethod(**{
            "label": "email",
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

    def test_site_data_validation(self):
        site_data = {
            "name": ("%s" % uuid.uuid1())[:30],
            "domain_id": self.domain_model.id,
            "description": "a super cool test site",
            "deletion_method_id": self.method_one.id,
            "deletion_method_data": {"en": "a"},
            "client_id": 0,
            "is_active": True,
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            site_model = crud(
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
            "client_id": 0,
            "is_active": True,
        }
        site_model = crud(
            model="Site",
            api_model=Site,
            data=site_data,
            action="create"
        )
