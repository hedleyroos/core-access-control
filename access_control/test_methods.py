from unittest import TestCase

from access_control import models
from access_control.db_actions import get_or_create


class GetOrCreateTestCase(TestCase):

    def test_get_or_create(self):
        # Successfully create a new object
        instance, created = get_or_create(models.Resource)
        self.assertTrue(instance is not None)
        self.assertTrue(created)

        # Return existing object
        instance, created = get_or_create(models.Resource, id=instance.id)
        self.assertTrue(instance is not None)
        self.assertFalse(created)
