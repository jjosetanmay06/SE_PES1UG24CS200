# Lab 5 – Static Code Analysis

## Project Overview
This lab focuses on identifying and fixing code quality, security, and style issues in a Python pharmacy stock management system.

## Project File
- `pharmacy_system.py` – Python implementation of the pharmacy stock management system.

## Tools Used
- **Pylint:** Checks code quality and reports potential errors and coding issues.
- **Bandit:** Identifies potential security vulnerabilities in Python code.
- **Flake8:** Checks Python code for style violations and formatting issues.

## Analysis Reports

The following files contain the static analysis results before and after fixing the issues.

| Tool | Before Fixes | After Fixes |
|---|---|---|
| Pylint | `pylint_before.txt` | `pylint_after.txt` |
| Bandit | `bandit_before.txt` | `bandit_after.txt` |
| Flake8 | `flake8_before.txt` | `flake8_after.txt` |

## Issues Addressed
- Replaced unsafe SQL query construction with parameterized queries.
- Improved exception handling.
- Removed unused imports and corrected code formatting.
- Improved input validation and code documentation.
- Applied Python naming conventions and structured the program using a main guard.

## Documentation
- `issues.md` – Summary of identified issues and their fixes.
- `reflection.md` – Reflection on the static analysis process and improvements.

## How to Run

Ensure Python and the required project dependencies are installed. Run the program using:

```bash
python pharmacy_system.py
```

## Conclusion
Static analysis helped improve the code's quality, readability, and security by identifying potential problems and verifying the fixes.
