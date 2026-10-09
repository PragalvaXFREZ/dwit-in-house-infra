# 4. Automate on GitHub

## Goal

Run the same checks on every proposed change, without relying on your laptop.

In **your fork**, create `.github/workflows/ci.yml` at the repository root. Write the workflow yourself using the requirements below and the [GitHub Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart).

## Workflow requirements

- Trigger on `push` and `pull_request`.
- Use a GitHub-hosted Ubuntu runner.
- Give the token only `contents: read`.
- Set a five-minute job timeout.
- Check out the code with persisted Git credentials disabled.
- Set up Python 3.11.
- Run shell steps from `learning/ci/demo`.
- Install the exact dependencies in `requirements-dev.txt`.
- Run lint, formatting and test checks using the commands from labs 2–3.
- Only if those checks pass, create and upload a source archive as a build artifact.

Use the official `actions/checkout`, `actions/setup-python` and `actions/upload-artifact` actions. Check their READMEs for inputs and pin each action to the full commit SHA of the release you select, with its release version in a comment.

For a small build step, Python can create a runnable zip application:

```bash
mkdir -p build
cp inventory.py build/__main__.py
python -m zipapp build -o inventory-checker.pyz
python inventory-checker.pyz examples/valid.json
```

Upload `learning/ci/demo/inventory-checker.pyz`, retaining it for one day.
An action's file-path input is relative to the workspace root; `defaults.run.working-directory` affects shell steps, not `uses` steps.

## Break and investigate

Open a PR in your fork that breaks a validation rule. Find the failed step and explain its logs.
Fix it with another commit. Download the successful artifact and run it locally with Python.
Do not hide failures using `continue-on-error` or `|| true`.

## Your challenge

Separate lint, test and build into jobs. Make build depend on both checks using `needs`.
Each job starts fresh: decide which setup steps must be repeated.
Explain the difference between a failed check and a rule that prevents merging. If your repository settings permit it, require your checks through a branch rule and verify it with a broken PR.

## Done when

A broken PR fails, the fix passes, and the artifact runs. No deployment, server credentials or self-hosted runner is needed.

Next: [our own runner](05-self-hosted-runner.md).
