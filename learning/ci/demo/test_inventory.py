"""Tests for the inventory validator."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from inventory import validate_inventory


class TestValidateInventory(unittest.TestCase):
    def test_one_server_with_valid_name(self):
        self.assertEqual(validate_inventory([{"name": "web-01"}]), [])

    def test_empty_name_is_invalid(self):
        self.assertTrue(validate_inventory([{"name": ""}]))

    def test_missing_name_is_invalid(self):
        self.assertTrue(validate_inventory([{}]))

    def test_whitespace_only_name_is_invalid(self):
        self.assertTrue(validate_inventory([{"name": "   "}]))

    def test_numeric_name_is_invalid(self):
        self.assertTrue(validate_inventory([{"name": 123}]))

    def test_non_list_inventory_is_invalid(self):
        self.assertTrue(validate_inventory({"name": "web-01"}))

    def test_non_object_server_is_invalid(self):
        self.assertTrue(validate_inventory(["web-01"]))

    def test_duplicate_server_names_are_invalid(self):
        servers = [{"name": "web-01"}, {"name": "web-01"}]
        self.assertTrue(validate_inventory(servers))

    def test_duplicate_names_with_whitespace_are_invalid(self):
        servers = [{"name": " web-01 "}, {"name": "web-01"}]
        self.assertTrue(validate_inventory(servers))

    def test_empty_inventory_is_valid(self):
        # An empty list is valid because it contains no invalid entries.
        self.assertEqual(validate_inventory([]), [])

    def test_cli_returns_nonzero_for_invalid_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            inventory_path = Path(temp_dir) / "invalid.json"

            inventory_path.write_text(
                json.dumps([{"name": ""}]),
                encoding="utf-8",
            )

            script_path = Path(__file__).with_name("inventory.py")

            result = subprocess.run(
                [sys.executable, str(script_path), str(inventory_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "name must be a non-empty string",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
