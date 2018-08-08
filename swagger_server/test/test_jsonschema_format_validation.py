# coding: utf-8

import jsonschema
import uuid
from unittest import TestCase


class TestExceptions(TestCase):

    def test_supported_formats(self):
        expected_supported_formats = [
            "email", "ip-address", "ipv4", "ipv6", "host-name", "hostname",
            "uri", "date-time", "regex", "date", "time", "uuid"
        ]
        self.assertEqual(expected_supported_formats,
                         list(jsonschema.FormatChecker.checkers.keys()))

    def test_uuid_format(self):
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(
                "not a uuid",
                {"type": "string", "format": "uuid"},
                format_checker=jsonschema.FormatChecker()
            )

        jsonschema.validate(
            str(uuid.uuid4()),
            {"type": "string", "format": "uuid"},
            format_checker=jsonschema.FormatChecker()
        )
