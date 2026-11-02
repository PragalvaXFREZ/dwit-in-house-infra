import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from inventory import validate_inventory


class TestInventory(unittest.TestCase):
    def test_valid_server_name(self):
        self.assertEqual(validate_inventory([{"name": "server1"}]), [])

    def test_empty_name(self):
        self.assertTrue(validate_inventory([{"name": ""}]))

    def test_missing_name(self):
        self.assertTrue(validate_inventory([{}]))

    def test_whitespace_only_name(self):
        self.assertTrue(validate_inventory([{"name": "   "}]))

    def test_numeric_name(self):
        self.assertTrue(validate_inventory([{"name": 123}]))

    def test_object_instead_of_list(self):
        self.assertTrue(validate_inventory({"name": "server1"}))

    def test_list_containing_non_object(self):
        self.assertTrue(validate_inventory(["server1"]))

    def test_duplicate_server_names(self):
        servers = [{"name": "server1"}, {"name": "server1"}]
        self.assertTrue(validate_inventory(servers))

    def test_empty_inventory_is_valid(self):
        # Decision: an empty inventory is acceptable.
        self.assertEqual(validate_inventory([]), [])

    def test_cli_invalid_inventory_returns_nonzero(self):
        demo_dir = Path(__file__).resolve().parent

        with tempfile.TemporaryDirectory() as temp_dir:
            inventory_file = Path(temp_dir) / "invalid.json"
            inventory_file.write_text(
                '[{"name": ""}]',
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(demo_dir / "inventory.py"),
                    str(inventory_file),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("name must be a non-empty string", result.stdout)


if __name__ == "__main__":
    unittest.main()
