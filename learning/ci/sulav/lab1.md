# Lab 1: Run locally (Sulav)

## What failed
Both `valid.json` and `invalid.json` exited with code 0. `invalid.json` has a
server with an empty name (`""`), but the validator accepted it.

## Why
The starter code only checked whether each server was a dictionary. It did not
check whether `name` existed, whether it was a string, or whether it was empty
or whitespace-only.

## How I fixed it
Added name checks in `validate_inventory`: a server fails if `name` is missing,
not a string, or empty/whitespace-only. The checks are an if/elif chain, so only
one name error is reported per server and a later check never runs on a value
that an earlier check already rejected (e.g. calling `.strip()` on a number).

## Break and investigate
| Input | Output | Exit code |
| --- | --- | --- |
| `valid.json` | Inventory is valid | 0 |
| `invalid.json` (empty name) | server 1: 'name' cannot be empty or whitespace-only | 1 |
| name is `42` | server 1: 'name' must be a string | 1 |
| 3 servers: good, no name, name `42` | server 2: missing 'name' field / server 3: 'name' must be a string | 1 |
| file does not exist | Cannot read inventory: [Errno 2] No such file or directory: 'examples/nope.json' | 1 |
| broken JSON (missing `]`) | Cannot read inventory: Expecting ',' delimiter: ... | 1 |

The missing file and broken JSON never reach `validate_inventory()`. Both are
caught by the `try`/`except` in `main()` because the input could not be read.
An invalid inventory is read successfully and then rejected by
`validate_inventory()` because the data is wrong. All three exit with 1, so CI
cannot tell them apart from the exit code alone.

## Extra rule: valid IP address
Rule: every server must have an `ip` field. It must be a string containing a
valid IPv4 or IPv6 address, checked with Python's `ipaddress` module. Numbers,
empty strings, out-of-range values like `192.0.2.300` and values with spaces are
rejected.

Why I check it is a string first: `ipaddress.ip_address()` silently accepts a
number like `5` and turns it into `0.0.0.5`. Without the check, a server with
`"ip": 5` would wrongly pass as valid.

Why I need `try`/`except`: `ipaddress.ip_address()` raises a `ValueError` for an
invalid IP instead of returning False. Catching it turns the crash into a normal
error message, so the remaining servers are still checked.

Design change: I first ended each name check with `continue`. That meant a
server with a bad name never had its IP checked, so `{"name": "", "ip": "hello"}`
reported only one error. I switched the name checks to an if/elif chain so both
errors are reported together.

## Why CI needs exit codes
CI needs an exit code to decide whether the program passed or failed: 0 means
it passed and anything else means it failed. It cannot rely on the printed
messages, because they differ between tools and can change. The exit code is a
standard every program follows. The printed message is for the human, to see
what went wrong and where.
