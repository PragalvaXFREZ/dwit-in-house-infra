\# Lab 1: Run Locally – Inventory Validation



\## Objective



Understand how the inventory validation program works, run it locally, identify errors, and understand how exit codes are used in automation.



\## 1. Python Virtual Environment



A virtual environment provides an isolated environment for installing Python packages without affecting the system-wide Python installation.



Commands used:



```powershell

py -m venv .venv

.venv\\Scripts\\Activate.ps1

```



\## 2. Inventory Validation



The `validate\_inventory()` function checks whether the inventory contains valid server information.



Validation rules implemented:



\- Inventory must be a JSON list.

\- Each server must be a JSON object.

\- Each server must have a `name` field.

\- The name must be a non-empty string.

\- Names containing only whitespace are invalid.

\- Server names must be unique after removing leading and trailing whitespace.

\- Name comparison is case-sensitive.



\## 3. Duplicate Name Validation



A Python set named `seen\_names` stores previously encountered server names.



The `strip()` method removes leading and trailing whitespace before comparison.



If a name already exists in the set, the program reports a duplicate name error.



\## 4. Error Handling



The program handles errors such as:



\- Missing inventory file.

\- Invalid JSON format.

\- Invalid server information.



\## 5. Exit Codes



\- Exit code `0`: Inventory is valid.

\- Exit code `1`: Inventory contains errors or cannot be read.



Automated CI/CD systems use exit codes to determine whether a step has passed or failed.



\## 6. Testing Performed



| Test | Expected result |

|---|---|

| Valid inventory | Success |

| Missing name | Validation error |

| Numeric name | Validation error |

| Whitespace-only name | Validation error |

| Duplicate server name | Validation error |

| Duplicate name with surrounding spaces | Validation error |

| Names with different letter cases | Success |

| Missing file | File error |

| Malformed JSON | JSON error |



All tests produced the expected results.



\## 7. Key Learnings



\- How to execute a Python program locally.

\- How to use a Python virtual environment.

\- How to read and validate JSON data.

\- How to handle file and JSON errors.

\- How to use sets to detect duplicate values.

\- Why exit codes are important in CI/CD automation.

\- Why validation logic should be separate from file reading and command-line output.

