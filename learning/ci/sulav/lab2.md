# Lab 2: Lint (Sulav)

## Setup
Installed Ruff 0.17.0 in the virtual environment and pinned it in
`sulav/requirements-dev.txt` as `ruff==0.17.0`. A fresh virtual environment in
`/tmp` installed it from the file and reported the same version, so anyone
(or CI) installing from the file gets the same Ruff.

## What failed first
`ruff check` passed, but `ruff format --check` failed (exit code 1) on my Lab 1
code. Two lines had trailing whitespace: a space after `errors.append(...)` on
line 24, and a blank line containing spaces on line 38. The code ran fine;
the spaces were invisible in my editor. `ruff format inventory.py` fixed them
and the check then passed (exit code 0).

## Break and investigate
| Change | `ruff check` | `ruff format --check` |
| --- | --- | --- |
| Added unused `import math` | Fails: F401 imported but unused (1) | Passes (0) |
| Changed `errors = []` to `errors=[ ]` | Passes (0) | Fails (1) |

The two commands check different things. `ruff check` looks for code that is
likely wrong or bad practice. `ruff format --check` only looks at layout, and
`ruff format` can always fix it automatically.

## Challenge: rule D103
D103 flags a public function with no docstring. Without one, someone using
the function has to read all of its code to know what it does and returns.

D103 is off by default: `ruff check` passed even though `main()` had no
docstring. I enabled it in `sulav/pyproject.toml`:

    [tool.ruff.lint]
    extend-select = ["D103"]

`extend-select` keeps Ruff's default rules and adds D103; `select` would
replace them. Ruff then reported D103 on `def main():` (exit code 1). I added
a docstring describing what `main()` does and which exit code means what, and
both checks passed.

## What linting cannot catch
I removed `.strip()` from the name check and gave `invalid.json` a name of
only spaces. `ruff check` and `ruff format --check` both passed, and the
program printed `Inventory is valid` with exit code 0, which is wrong.

Ruff compares code against known bad patterns. `server["name"] == ""` is
normal Python, and it is only wrong because of my rule that whitespace-only
names are invalid, which Ruff does not know. Only I noticed, because I knew
the expected result. A test can write that expectation down and check it
automatically (Lab 3). I undid the change with `git restore`.
