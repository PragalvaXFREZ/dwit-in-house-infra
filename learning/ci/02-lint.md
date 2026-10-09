# 2. Add linting

## Goal

Catch code issues without relying on a person noticing them.

With your virtual environment active:

```bash
python -m pip install ruff
python -m ruff check inventory.py
python -m ruff format --check inventory.py
```

Find the installed version with `python -m ruff --version`. Record it in a new `requirements-dev.txt` using an exact `ruff==VERSION` entry. Confirm a fresh virtual environment can install it with `python -m pip install -r requirements-dev.txt`. Commit that file.

## Break and investigate

Add an unused `import math` to `inventory.py`. Run the linter and inspect its exit code.
Remove the import, introduce inconsistent formatting, then run the formatter check.
Use `python -m ruff format inventory.py` to fix formatting.

## Your challenge

Choose a Ruff rule, explain what problem it catches, and demonstrate a violation and fix.
Put any configuration in `pyproject.toml` inside this demo directory.

## Done when

Lint and formatting checks pass. Can they prove your name-validation rule works? Demonstrate a logic bug they miss, then undo it.

Next: [tests](03-test.md).
