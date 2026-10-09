# CI, one step at a time

Build a small tool, decide how to check it, then automate those checks.

Our project is a Python CLI that validates a fictional server inventory. It reads a JSON file; it does not contact or configure any machines. Use fake data throughout.

## Before starting

You need Git, Python 3.11 or newer, and basic Python functions, lists and loops. Review the [Git guide](../git/git-github-guide.md) if branches and commits are new.

You do not need push access to this repository. Work in your own fork and hand your work back as a pull request.

## Fork, work, hand in

1. On GitHub, open this repository and click **Fork** (top right). Keep the default settings. GitHub creates a copy under your own account.
2. Clone **your fork**, not this repository, then make a branch for the labs:

   ```bash
   git clone https://github.com/<your-username>/dwit-in-house-infra.git
   cd dwit-in-house-infra
   git checkout -b ci-labs
   ```

3. Commit after each lab and push to your fork with `git push -u origin ci-labs`.
4. To hand in, open your fork on GitHub and click **Contribute → Open pull request**. Target this repository's `main` branch. Your mentor reviews it there; it will not be merged, and that is fine.

Run commands from `learning/ci/demo/` unless a lab says otherwise. Linux/macOS commands are shown; on Windows use `py` to create the environment, `.venv\Scripts\activate` to activate it, and `echo $LASTEXITCODE` in PowerShell wherever a lab uses `echo $?`.

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
