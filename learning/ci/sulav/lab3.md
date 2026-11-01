# Lab 3: Test (Sulav)

## Setup
Created `sulav/test_inventory.py` with `unittest`. Valid input uses
`assertEqual(result, [])`; invalid input uses `assertTrue(result)` (at least
one error), so rewording a message does not break a test.

## What failed first
My valid-server test had no `ip` and failed, because my Lab 1 IP rule requires
one. The test was wrong, not the code. Every invalid test now keeps the other
fields valid and breaks only one thing.

## Tests
| Test | Protects |
| --- | --- |
| valid server accepted | good input is not rejected |
| empty / missing / whitespace / numeric name | each part of the name check |
| object instead of list, non-object in list | input structure checks |
| missing / non-string / invalid ip | each part of the IP rule |
| empty inventory rejected | empty-inventory rule |
| CLI rejects invalid file | nonzero exit code CI relies on |

## Break and investigate
With the name check commented out, the 4 name tests failed (`[] is not true`)
and the other 3 passed. Both Ruff checks still passed: lint checks how code
looks, tests check what it does. Restored with `git restore`.

## Challenges
**IP rule:** my missing-ip test used `"ip": ""`, so it was really testing the
address check. Breaking only that check exposed it; I removed the `ip` key.

**Empty inventory:** rejected, since an empty file is more likely a mistake.
The test failed first, then I added this after the list check and it passed:

    if len(servers) == 0:
        return ["inventory cannot be empty"]

**CLI test:** runs the tool with `subprocess.run` and checks the exit code is
not 0 and the empty-name message is in `stdout` (the tool uses `print()`, not
`stderr`). `check=False` added for Ruff PLW1510, since a nonzero exit is
expected.
