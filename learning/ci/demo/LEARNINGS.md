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

### Virtual Environment and Installation

- `py -3 -m venv .venv`
- `& .\.venv\Scripts\Activate.ps1`
- `python -m pip install ruff==0.17.0`
- `python -m ruff --version`

### Linting and Formatting

- `python -m ruff check .`
- `python -m ruff check inventory.py`
- `python -m ruff check --fix inventory.py`
- `python -m ruff format --check .`
- `python -m ruff format .`
- `python -m ruff format inventory.py`

### Testing and Verification

- `python -m py_compile inventory.py`
- `python inventory.py examples/valid.json`
- `python -m unittest discover -s . -p "test_*.py" -v`

## Testing and Verification

- Installed Ruff version `0.17.0` in a Python virtual environment.
- Configured Ruff using `pyproject.toml`.
- Ran Ruff linting and confirmed that all checks passed.
- Ran the formatting check and found formatting inconsistencies in `inventory.py`.
- Used Ruff formatting to automatically correct the inconsistencies.
- Ran the formatting check again and confirmed that all five Python files were formatted.
- Compiled `inventory.py` successfully.
- Executed the inventory program and received the output `Inventory is valid`.
- Ran the unit test suite and confirmed that all 10 tests passed.

## Key Takeaway

Linting and formatting help maintain consistent, readable Python code. Using Ruff in a CI pipeline allows code quality issues and formatting inconsistencies to be detected automatically before code is merged.