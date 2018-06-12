import json
import uuid

from ge_core_shared import db_actions

from access_control import models
from project.settings import API_KEY_HEADER
from swagger_server.test import BaseTestCase
from swagger_server.models.domain import Domain
from swagger_server.models.site import Site


class TestGetSitesUnderDomain(BaseTestCase):

    def setUp(self):
        """
        Top Level Domain
         |
         +-- Child Domain 1
         |    |
         |    +-- Site 1
         |    +-- Site 2
         |
         +-- Child Domain 2
              |
              +-- Site 3
        :return:
        """
        models.UserSiteRole.query.delete()
        models.SiteRole.query.delete()
        models.Site.query.delete()
        models.UserDomainRole.query.delete()
        models.DomainRole.query.delete()
        models.Domain.query.delete()
        # Parent Domain
        self.top_level_domain_data = {
            "name": "The Top Level Domain",
            "description": "The Top Level Domain",
        }
        self.top_level_domain = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.top_level_domain_data,
            action="create"
        )
        # Child Domain 1
        self.child_domain_data = {
            "name": "Child Domain 1",
            "description": "The 1st Child Domain",
            "parent_id": self.top_level_domain.id
        }
        self.child_domain_1 = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.child_domain_data,
            action="create"
        )
        # Child Domain 2
        self.child_domain_data = {
            "name": "Child Domain 2",
            "description": "The 2nd Child Domain",
            "parent_id": self.top_level_domain.id
        }
        self.child_domain_2 = db_actions.crud(
            model="Domain",
            api_model=Domain,
            data=self.child_domain_data,
            action="create"
        )
        # Site 1
        self.site_data = {
            "name": "Site 1",
            "domain_id": self.child_domain_1.id,
            "description": "Site 1",
            "is_active": True,
        }
        self.site_1 = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )
        # Site 2
        self.site_data = {
            "name": "Site 2",
            "domain_id": self.child_domain_1.id,
            "description": "Site 2",
            "is_active": True,
        }
        self.site_2 = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )
        # Site 3
        self.site_data = {
            "name": "Site 3",
            "domain_id": self.child_domain_2.id,
            "description": "Site 3",
            "is_active": True,
        }
        self.site_3 = db_actions.crud(
            model="Site",
            api_model=Site,
            data=self.site_data,
            action="create"
        )
        self.headers = {API_KEY_HEADER: "test-api-key"}

    def test_get_sites_under_domain(self):
        """Test case for get_sites_under_domain
        """
        response = self.client.open(
            "/api/v1/ops/get_sites_under_domain/{domain_id}".format(
                domain_id=self.top_level_domain.id
            ), method='GET', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        r_data = json.loads(response.data)
        site_names = [site["name"] for site in r_data]
        self.assertEqual(sorted(site_names), sorted(["Site 1", "Site 2", "Site 3"]))
        site_ids = [site["id"] for site in r_data]
        self.assertEqual(sorted(site_ids),
                         sorted([self.site_1.id, self.site_2.id, self.site_3.id]))

        response = self.client.open(
            "/api/v1/ops/get_sites_under_domain/{domain_id}".format(
                domain_id=self.child_domain_1.id
            ), method='GET', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        r_data = json.loads(response.data)
        site_names = [site["name"] for site in r_data]
        self.assertEqual(sorted(site_names), sorted(["Site 1", "Site 2"]))
        site_ids = [site["id"] for site in r_data]
        self.assertEqual(sorted(site_ids),
                         sorted([self.site_1.id, self.site_2.id]))

        response = self.client.open(
            "/api/v1/ops/get_sites_under_domain/{domain_id}".format(
                domain_id=self.child_domain_2.id
            ), method='GET', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        r_data = json.loads(response.data)
        site_names = [site["name"] for site in r_data]
        self.assertEqual(site_names, ["Site 3"])
        site_ids = [site["id"] for site in r_data]
        self.assertEqual(sorted(site_ids), [self.site_3.id])


if __name__ == '__main__':
    import unittest
    unittest.main()
