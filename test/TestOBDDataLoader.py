import json
import unittest
from utils.DataTypes import load_datatypes_from_json, DisplayMeterSerial


class TestOBDDataLoader(unittest.TestCase):

    def setUp(self):
        # A valid JSON snippet for testing
        self.valid_json = """
        {
          "engine_rpm": {
            "name": "Engine RPM",
            "min_value": 0,
            "max_value": 8000,
            "default_unit": "RPM",
            "alternate_units": ["r/min"],
            "default_display_type": "circular_gauge",
            "alternate_display_types": ["plain_text"]
          }
        }
        """

    def test_successful_load(self):
        """Test that valid JSON is parsed correctly into DataType objects."""
        data = load_datatypes_from_json(self.valid_json)

        self.assertIn("engine_rpm", data)
        rpm = data["engine_rpm"]

        # Check basic fields
        self.assertEqual(rpm.name, "Engine RPM")
        self.assertEqual(rpm.max_value, 8000)

        # Check Enum conversion
        self.assertIsInstance(rpm.default_display_type, DisplayMeterSerial)
        self.assertEqual(rpm.default_display_type, DisplayMeterSerial.CIRCULAR_GAUGE)
        self.assertEqual(rpm.alternate_display_types[0], DisplayMeterSerial.PLAIN_TEXT)

    def test_invalid_enum_value(self):
        """Test that an unknown display type raises a ValueError."""
        invalid_json = """
        {
          "speed": {
            "name": "Speed",
            "min_value": 0,
            "max_value": 100,
            "default_unit": "mph",
            "alternate_units": [],
            "default_display_type": "vertical_bar_graph", 
            "alternate_display_types": []
          }
        }
        """
        # "vertical_bar_graph" is not in the DisplayMeter Enum, so this should fail
        with self.assertRaises(ValueError):
            load_datatypes_from_json(invalid_json)

    def test_missing_field(self):
        """Test that missing required keys raise a KeyError."""
        missing_key_json = """
        {
          "speed": {
            "name": "Speed",
            "min_value": 0,
            "default_unit": "mph", 
            "alternate_units": [],
            "default_display_type": "circular_gauge",
            "alternate_display_types": []
          }
        }
        """
        # "max_value" is missing
        with self.assertRaises(KeyError):
            load_datatypes_from_json(missing_key_json)

    def test_malformed_json(self):
        """Test that invalid JSON syntax raises a JSONDecodeError."""
        bad_syntax = "{ 'name': 'Speed' "  # Missing closing brace/quotes
        with self.assertRaises(json.JSONDecodeError):
            load_datatypes_from_json(bad_syntax)


if __name__ == '__main__':
    unittest.main()