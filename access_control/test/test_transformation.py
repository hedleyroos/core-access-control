from datetime import date, timedelta
from unittest import TestCase
from ge_core_shared.transformation import Mapping, Transformation


def tomorrow(today: date) -> date:
    return today + timedelta(days=1)


class TestTransformation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transformation = Transformation([
            # Copy key and value
            Mapping("verbatim"),
            # Copy value to a new field
            Mapping("old_name", "new_name"),
            # Convert a value using a specified function
            Mapping("name", "uppercase_name", lambda x: x.upper()),
            # Convert a value. Use same field name.
            Mapping("sneaky", conversion=lambda x: x[::-1]),
            # Conversion function working on dates
            Mapping("today", output_field="tomorrow", conversion=tomorrow),
            # Fields without mappings are not included in the result
        ])

    def test_transformations(self):
        data = {
            "verbatim": "the same",
            "old_name": "getting a new name",
            "name": "Adam",
            "sneaky": "0123456789",
            "no_map": "I'm disappearing",
            "today": date.today()
        }
        expected = {
            "verbatim": "the same",
            "new_name": "getting a new name",
            "uppercase_name": "ADAM",
            "sneaky": "9876543210",
            "tomorrow": date.today() + timedelta(days=1)
        }
        self.assertEqual(expected, self.transformation.apply(data))

    def test_bad_data(self):
        bad_data = {
            "name": 1,  # Name should be a string
        }
        with self.assertRaises(RuntimeError):
            self.transformation.apply(bad_data)

    def test_copy_fields(self):
        data = {
            "verbatim": "the same",
            "old_name": "getting a new name",
            "name": "Adam",
            "sneaky": "0123456789",
            "no_map": "I'm disappearing",
            "today": date.today()
        }
        # The copy_fields argument is a convenience mechanism
        copy_transform = Transformation(
            copy_fields=data.keys()
        )
        self.assertEqual(data, copy_transform.apply(data))

    def test_duplicate_input_fields(self):
        with self.assertRaises(RuntimeError):
            Transformation([
                Mapping("a"),
                Mapping("b"),
                Mapping("a"),  # Duplicate
            ])

        with self.assertRaises(RuntimeError):
            Transformation(mappings=[Mapping("a"), Mapping("b")],
                           copy_fields=["b"])  # Duplicate

        # For output fields
        with self.assertRaises(RuntimeError):
            Transformation([
                Mapping("a", "c"),
                Mapping("b"),
                Mapping("c"),  # Implied output field "c" already specified
            ])
