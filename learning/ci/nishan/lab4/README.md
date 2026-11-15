\# Lab 4: CI Pipeline with GitHub Actions



\## Objective



Automate code quality checks, unit tests, and application packaging using GitHub Actions.



\## Workflow



The workflow is located at:



`.github/workflows/ci.yml`



It runs automatically on every push and pull request.



\### Workflow steps



1\. Checkout the repository using `actions/checkout`.

2\. Set up Python 3.11 using `actions/setup-python`.

3\. Install development dependencies from `requirements-dev.txt`.

4\. Run Ruff linting.

5\. Check code formatting with Ruff.

6\. Run unit tests using Python's `unittest`.

7\. Build an executable Python zipapp.

8\. Upload the zipapp as a GitHub Actions artifact.



The workflow uses `ubuntu-latest`, has a five-minute timeout, and grants only `contents: read` permission. The checkout step disables credential persistence.



\## Local Validation



The following commands were used to verify the lab:



```powershell

py -m ruff check .

py -m ruff format --check .

py -m unittest discover -s . -p "test\_\*.py" -v

```



Results:



\- Ruff lint: Passed

\- Ruff format: Passed

\- Unit tests: 11 passed



\## Build and Run the Zipapp



The workflow packages `inventory.py` into `inventory-checker.pyz`.



Build locally:



```powershell

New-Item -ItemType Directory -Force build

Copy-Item inventory.py build\\\_\_main\_\_.py

py -m zipapp build -o inventory-checker.pyz

```



Run the archive:



```powershell

py inventory-checker.pyz examples\\valid.json

```



Expected output:



```text

Inventory is valid

```



The generated `.pyz` file is ignored by Git and uploaded by GitHub Actions as an artifact with a one-day retention period.



\## CI Checks and Pull Requests



A failed workflow check indicates that one or more automated steps did not pass. A branch protection rule or ruleset can separately require selected checks to pass before a pull request can be merged.



A failed check does not automatically block merging unless repository rules require it.



\## Challenge: Separate Jobs



The workflow can be extended into separate `lint`, `test`, and `build` jobs.



\- `lint`: runs Ruff checks.

\- `test`: runs unit tests.

\- `build`: depends on both `lint` and `test` using `needs`.



Each job runs on a fresh runner, so Python setup and dependency installation must be repeated in each job that needs them. The build job should run only after both lint and test jobs succeed.



\## Conclusion



This lab demonstrates how GitHub Actions can automate code validation, testing, packaging, and artifact upload to improve the reliability of a Python project.

