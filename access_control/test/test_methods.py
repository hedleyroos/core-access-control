from unittest import TestCase

from ge_core_shared.db_actions import get_or_create, delete_entry, list_entry

from access_control import models

URN = "urn:test:me"


class GetOrCreateTestCase(TestCase):

    def test_get_or_create(self):
        try:
            delete_entry(models.Resource, query={"urn": URN})
        except Exception:
            pass

        # Successfully create a new object
        instance, created = get_or_create(models.Resource, urn=URN, description="Test")
        self.assertTrue(instance is not None)
        self.assertTrue(created)

        # Return existing object
        instance, created = get_or_create(models.Resource, id=instance.id, urn=URN)
        self.assertTrue(instance is not None)
        self.assertFalse(created)


class ListFiltersTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a few domains.
        try:
            delete_entry(models.Domain, query={"name": "Domain 2"})
        except Exception:
            pass
        try:
            delete_entry(models.Domain, query={"name": "Domain 1"})
        except Exception:
            pass
        cls.domain_1, created = get_or_create(
            models.Domain, name="Domain 1"
        )
        cls.domain_2, created = get_or_create(
            models.Domain, name="Domain 2", parent_id=cls.domain_1.id
        )

    def test_list_entry(self):
        # Test get unfiltered list.
        entries = list_entry(
            models.Domain,
            query={
                "order_by": ["id"]
            }
        )
        # Maybe more than the two created but at least 2.
        self.assertGreaterEqual(len(entries), 2)
        # Test get list with single model id.
        entries = list_entry(
            models.Domain,
            query={
                "ids": {
                    "id": self.domain_1.id
                },
                "order_by": ["id"]
            }
        )
        self.assertEquals(len(entries), 1)
        # Test get list with model ids and an additional filter.
        entries = list_entry(
            models.Domain,
            query={
                "ids": {
                    "id": [self.domain_1.id, self.domain_2.id],
                    "parent_id": self.domain_1.id
                },
                "order_by": ["id"]
            }
        )
        self.assertEquals(len(entries), 1)
        self.assertEquals(entries[0][0].id, self.domain_2.id)
