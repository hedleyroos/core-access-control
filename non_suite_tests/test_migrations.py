import datetime
from unittest import TestCase

from access_control import models


DB = models.DB


class SiteModelValidationTestCase(TestCase):

    def test_sites_exist(self):
        sites = DB.session.get_bind().execute("SELECT * FROM site;")
        self.assertEqual(sites.rowcount, 19)


    def test_site_deletion_method_id(self):
        index = 0
        sites = DB.session.get_bind().execute("SELECT * FROM site;")
        for site in sites:
            self.assertEqual(site["deletion_method_id"], 0)
