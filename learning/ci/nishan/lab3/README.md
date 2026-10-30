# Lab 3: Write Tests

## What I Learned

- Python's built-in `unittest` framework is used to test program behavior.
- Assertions check whether actual results match expected results.
- Tests can detect incorrect behavior even when Python code is syntactically valid.
- `subprocess.run` allows tests to execute a command-line program and check its exit code.
- Temporary directories allow tests to create temporary files safely.
- An empty inventory is considered valid in this implementation.
- Duplicate server names are rejected.
- Server names with surrounding whitespace are also treated as duplicates because the inventory validator uses `.strip()`.
- Automated tests help identify errors and prevent regressions when code changes.

## Testing Commands

- `python -m unittest discover -s . -p "test_*.py" -v`
- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m py_compile inventory.py`

## Test Cases Implemented

1. Valid server name.
2. Empty server name.
3. Missing server name.
4. Whitespace-only server name.
5. Numeric server name.
6. Non-list inventory.
7. Non-object server entry.
8. Duplicate server names.
9. Duplicate names with surrounding whitespace.
10. Empty inventory.
11. CLI returns a nonzero exit code for invalid inventory.

## Testing and Verification

- Successfully executed all 11 unit tests.
- Verified that valid inventory data is accepted.
- Verified that invalid inventory data is rejected.
- Tested duplicate server names, including names with surrounding whitespace.
- Tested the command-line program using a temporary JSON file.
- Confirmed that the test suite completed without failures.

## Key Takeaway

Automated testing verifies correct behavior for valid and invalid inputs. Unit tests help identify problems early and prevent existing functionality from breaking when code is modified.