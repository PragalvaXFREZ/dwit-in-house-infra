## Setup
Created `.github/workflows/ci.yml` at the repo root on a `lab4` branch made from
`lab3`, so CI has my tests to run. Actions was already enabled on my fork.

The workflow runs on `push` and `pull_request` on `ubuntu-latest`, with a
read-only token (`contents: read`), a 5-minute timeout and
`working-directory: learning/ci/sulav`. Each action is pinned to a full commit
SHA with its version in a comment (checkout v7.0.1, setup-python v7.1.0,
upload-artifact v7.0.2), because a tag can be moved but a SHA cannot.

## Steps
| Step | Does |
| --- | --- |
| checkout (`persist-credentials: false`) | copies the repo onto the empty runner without leaving the token behind |
| setup-python `"3.11"` | installs 3.11; quoted so YAML does not read it as a number |
| install | `pip install -r requirements-dev.txt` (ruff 0.17.0) |
| lint / format check | the Ruff commands from lab 2 |
| tests | the `unittest` command from lab 3 |
| build | packs `inventory.py` into `inventory-checker.pyz` and runs it on `valid.json` |
| upload | saves the `.pyz` as an artifact for 1 day |

A job stops at the first failing step, so the build only runs if lint, format
and tests pass. No extra code was needed for that.

## What failed first
I ran `pip install` from `.github/workflows` and got "No such file", because
`requirements-dev.txt` is in `sulav`. Same reason the workflow needs
`working-directory`. Before pushing I also fixed `rum:` instead of `run:` and
one step indented 12 spaces instead of 6; either would have made the workflow
invalid. All checks passed locally (12 tests) and the first run was green.

## Break and investigate
On `lab4-break` I commented out the name check and opened PR #1 in my fork,
with base `lab4` so it only showed this change. Lint and format passed, 5 of 12
tests failed (the 4 name tests and the CLI test), and build and upload were
skipped. This matched my local run.

- `[] is not true`: `validate_inventory` returned no errors for a bad name.
- `0 == 0`: the CLI exited 0 on invalid input.

I restored the check in a new commit and the PR went green.

## Silent failure
The green run had no artifact, only a warning: "No files were found with the
provided path: inventory-checker.pyz". `working-directory` only applies to
`run:` steps; a `uses:` step's path starts at the repo root. Fixed with:

    path: learning/ci/sulav/inventory-checker.pyz
    if-no-files-found: error

Now a missing artifact fails the run instead of passing with a warning. A green
check is not proof the output exists.

## Artifact
Downloaded `inventory-checker.pyz` from the green run and ran it locally.
`valid.json` printed "Inventory is valid" (exit 0); `invalid.json` printed
"server 1: 'name' cannot be empty or whitespace-only" (exit 1). Then merged
PR #1 into `lab4`.

## Challenges
**Separate jobs:** split into `lint`, `test` and `build`, with
`needs: [lint, test]` on `build`. Each job starts on a fresh machine, so each
one repeats checkout and setup-python. I first left those out of some jobs.
`test` skips `pip install`: `requirements-dev.txt` only has ruff and
`unittest` is built in. `build` does not re-run checks because `needs` already
guarantees they passed. `lint` and `test` now run in parallel (7s each), then
`build` (6s).

**Failed check vs merge rule:** a failed check only reports. On PR #1 every
check was red but the Merge button still worked. A branch rule blocks the
merge.

**Branch rule:** added a ruleset on `lab4` requiring `lint`, `test` and
`build`, blocking force pushes and deletions, with an empty bypass list. I left
"Restrict updates" off, since with no bypass it would block every merge. Tested
with another broken PR: `test` failed, `build` was skipped, every check showed
"Required" and Merge was disabled. Closed it without merging.

All three checks are required because a skipped check does not block a merge.
If only `build` were required, a failing test would skip it and the PR could
still be merged. Side effect: I can no longer push straight to `lab4`, so
these notes went in through a PR.
