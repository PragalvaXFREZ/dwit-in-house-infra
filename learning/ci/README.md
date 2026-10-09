# CI, one step at a time

Build a small tool, decide how to check it, then automate those checks.

Our project is a Python CLI that validates a fictional server inventory. It reads a JSON file; it does not contact or configure any machines. Use fake data throughout.

## Before starting

You need Git, Python 3.11 or newer, and basic Python functions, lists and loops. Review the [Git guide](../git/git-github-guide.md) if branches and commits are new.

Fork this repository for labs 1–4. Clone your fork and make a working branch. Run commands from `learning/ci/demo/` unless a lab says otherwise. Linux/macOS commands are shown; on Windows use `py` to create the environment and `.venv\Scripts\activate` to activate it.

## The five labs

| Lab | Build | Evidence to keep |
| --- | --- | --- |
| [1. Run locally](01-run-locally.md) | Your first validation rule | Valid and invalid inputs with their exit codes |
| [2. Lint](02-lint.md) | Automated code checks | A lint failure and its fix |
| [3. Test](03-test.md) | Behaviour checks | A failing test, then a passing test |
| [4. Automate](04-github-actions.md) | Your own GitHub-hosted workflow | A failed PR check, a fixed check and a downloadable artifact |
| [5. Host a runner](05-self-hosted-runner.md) | A supervised, isolated runner | The same checks running on a lab VM |

Commit after each lab. Include a short note: what failed, why, and how you fixed it.
The starter intentionally lacks name validation. There is no completed workflow to copy.

CI means automatically checking changes as they are integrated. A runner is the machine executing those checks. Building an artifact is not deployment; deployment is outside this exercise.
