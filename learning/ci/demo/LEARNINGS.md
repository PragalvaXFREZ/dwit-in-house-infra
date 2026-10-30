# Lab 2: Add Linting

## What I Learned

- Linting helps detect code issues such as unused imports and disorganized imports.
- Ruff is a Python tool used for linting and code formatting.
- `ruff check` checks Python files for potential issues.
- `ruff format --check` checks formatting without modifying files.
- `ruff format` automatically fixes formatting inconsistencies.
- Ruff returns exit code 1 when linting errors are found and 0 when the check passes.
- `requirements-dev.txt` records development dependencies with exact versions, such as `ruff==0.17.0`.
- A fresh virtual environment can install dependencies using `python -m pip install -r requirements-dev.txt`.
- `pyproject.toml` can be used to configure Ruff rules.
- Ruff rule `F401` detects unused imports, while `B007` detects unused loop-control variables.

## Commands Practiced

- `python -m ruff --version`
- `python -m ruff check inventory.py`
- `python -m ruff check --fix inventory.py`
- `python -m ruff format --check inventory.py`
- `python -m ruff format inventory.py`
- `python -m pip install -r requirements-dev.txt`

## Testing and Verification

- Introduced an unused `math` import and observed Ruff report the issue.
- Checked the exit code after a linting failure.
- Removed the unused import and verified that linting passed.
- Introduced inconsistent spacing and used Ruff to correct the formatting.
- Configured rule `B007`, demonstrated a violation, and fixed it.
- Tested the pinned Ruff version in a fresh virtual environment.

## Key Takeaway

Linting and formatting help maintain consistent, readable Python code and allow CI pipelines to detect problems automatically before code is merged.