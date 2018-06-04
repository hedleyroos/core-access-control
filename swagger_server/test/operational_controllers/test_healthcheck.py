import json

from swagger_server.test import BaseTestCase


class TestHealthCheck(BaseTestCase):

    def test_healthcheck(self):
        """Test case for healthcheck
        """
        response = self.client.open("/api/v1/ops/healthcheck", method="GET",
                                    headers={})  # No API key
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for e in ["host", "server_timestamp", "db_timestamp", "version"]:
            self.assertIn(e, data)


if __name__ == '__main__':
    import unittest
    unittest.main()
