"""Validate a fictional server inventory; no network access is performed."""

import argparse
import json
from pathlib import Path


def validate_inventory(servers):
    """Return validation errors. An empty list means the inventory is valid."""
    if not isinstance(servers, list):
        return ["inventory must be a JSON list"]

    errors = []
    for index, server in enumerate(servers, start=1):
        if not isinstance(server, dict):
            errors.append(f"server {index}: must be a JSON object")
            continue
        # TODO (lab 1): reject missing, non-string, empty or whitespace-only names.
        # Add your own validation rule after implementing the name check.
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="path to a JSON inventory")
    args = parser.parse_args()
    try:
        servers = json.loads(args.inventory.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Cannot read inventory: {error}")
        return 1

    errors = validate_inventory(servers)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Inventory is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
