from unittest import TestCase

from ge_core_shared.db_actions import get_or_create, delete_entry

from access_control import models

URN = "urn:test:me"


class GetOrCreateTestCase(TestCase):

    def test_get_or_create(self):
        try:
            delete_entry(models.Resource, query={"urn": URN})
        except Exception:
            pass

        # Successfully create a new object
        instance, created = get_or_create(models.Resource, urn=URN)
        self.assertTrue(instance is not None)
        self.assertTrue(created)

        # Return existing object
        instance, created = get_or_create(models.Resource, id=instance.id, urn=URN)
        self.assertTrue(instance is not None)
        self.assertFalse(created)
