# 3. Write tests

## Goal

Check behaviour, including cases that look like valid Python but give the wrong answer.

Create `test_inventory.py` using Python's built-in `unittest`. Import `validate_inventory` from `inventory` and pass it Python values directly. Start with these cases:

| Input | Expected result |
| --- | --- |
| One server with a non-empty name | No errors |
| A server with an empty name | At least one error |
| Missing name | At least one error |
| Whitespace-only name | At least one error |
| A numeric name | At least one error |
| A JSON object instead of a list | At least one error |
| A list containing a non-object | At least one error |

```bash
python -m unittest discover -s . -p 'test_*.py' -v
python -m ruff check .
python -m ruff format --check .
```

## Break and investigate

Temporarily remove the name check. The tests should fail even though lint may pass.
Restore it and run again. Read the test count: zero tests passing is not evidence of correctness.

## Your challenge

Write a failing test for the extra rule you chose in lab 1. Fix the implementation if needed.
Decide whether an empty inventory is acceptable and document that decision in a test.
Add one CLI test using `subprocess.run` to check that invalid input produces a nonzero exit code.

## Done when

You have demonstrated a real failing test followed by a fix. Explain which behaviour each test protects.

Next: [GitHub Actions](04-github-actions.md).
