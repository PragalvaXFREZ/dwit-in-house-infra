# 1. Run locally

## Goal

Understand the program before automating it.

```bash
cd learning/ci/demo
python3 -m venv .venv
source .venv/bin/activate
python inventory.py examples/valid.json
echo $?
python inventory.py examples/invalid.json
echo $?
```

Both inputs currently pass. That is the intentional bug: the starter checks the JSON structure but does not check server names.

## Build

Implement the TODO in `validate_inventory`:
- Every server needs a `name`.
- The name must be a string containing at least one non-whitespace character.
- Return a useful error identifying the server when the rule fails.

Keep validation separate from reading files and printing output. The CLI already translates an empty error list into exit code 0 and validation errors into exit code 1.

## Break and investigate

Try a missing file and malformed JSON. Compare those errors with an invalid inventory.
Change the invalid example locally to try a missing name, a number and whitespace.

## Your challenge

Choose one additional rule and implement it: valid IP addresses, duplicate names, or allowed roles.
Write down your rule precisely before coding it. Use Python's `ipaddress` module if you choose IP validation.

## Done when

The valid example exits 0, the invalid example exits 1, and you can explain why an automated tool needs an exit code rather than just a printed message.

Next: [linting](02-lint.md).
