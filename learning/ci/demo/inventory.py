"""Validate a fictional server inventory; no network access is performed."""

import argparse
import json
from pathlib import Path


def validate_inventory(servers):
    """Return validation errors. An empty list means the inventory is valid."""
    if not isinstance(servers, list):
        return ["inventory must be a JSON list"]

    errors = []
    names = set()

    for index, server in enumerate(servers, start=1):
        if not isinstance(server, dict):
            errors.append(f"server {index}: must be a JSON object")
            continue

        if "name" not in server:
            errors.append(f"server {index}: missing name")
            continue

        name = server["name"]

        if not isinstance(name, str) or not name.strip():
            errors.append(f"server {index}: name must be a non-empty string")
            continue

        # Extra rule: server names must be unique.
        if name in names:
            errors.append(f"server {index}: duplicate name '{name}'")
        else:
            names.add(name)

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
