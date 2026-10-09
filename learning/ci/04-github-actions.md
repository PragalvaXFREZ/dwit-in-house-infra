# 4. Automate on GitHub

## Goal

Run the same checks on every proposed change, without relying on your laptop.

In **your fork**, create `.github/workflows/ci.yml` at the repository root. Write the workflow yourself using the requirements below and the [GitHub Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart).

GitHub disables workflows on a fresh fork. Before pushing your workflow, open your fork's **Actions** tab and click **I understand my workflows, go ahead and enable them**. If you skip this, pushing `ci.yml` does nothing and no run appears.

## Workflow requirements

- Trigger on `push` and `pull_request` (the `on:` key).
- Use a GitHub-hosted Ubuntu runner (`runs-on:`).
- Give the token only `contents: read` (a top-level `permissions:` block).
- Set a five-minute job timeout (`timeout-minutes:` on the job).
- Check out the code with persisted Git credentials disabled (the `persist-credentials` input of `actions/checkout`, under `with:`).
- Set up Python 3.11 (the `python-version` input of `actions/setup-python`).
- Run shell steps from `learning/ci/demo` (`defaults.run.working-directory` on the job).
- Install the exact dependencies in `requirements-dev.txt`.
- Run lint, formatting and test checks using the commands from labs 2–3.
- Only if those checks pass, create and upload a source archive as a build artifact.

Use the official `actions/checkout`, `actions/setup-python` and `actions/upload-artifact` actions. Check their READMEs for inputs and pin each action to the full commit SHA of the release you select, with its release version in a comment.

To find that SHA: open the action's repository on GitHub, click **Releases**, pick a version, and click the short commit hash shown next to the tag. The page that opens shows the full 40-character SHA. Use it like this:

```yaml
- uses: actions/checkout@<full-40-character-sha> # v4.2.2
```

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
