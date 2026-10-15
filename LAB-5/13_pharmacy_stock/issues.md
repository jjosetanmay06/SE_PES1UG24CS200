# Lab 5 – Static Code Analysis

## Issues Identified and Fixed

| Issue | Type | Original Finding | Fix Applied |
|---|---|---|---|
| SQL injection risk | Security | SQL query constructed using string formatting | Used a parameterized SQL query with placeholders |
| Broad exception handling in `dispense()` | Bug | Bare `except:` hid unexpected errors | Replaced broad exception handling with explicit validation |
| Broad exception handling in `load_stock()` | Reliability | Stock-loading errors were silently ignored | Handled file and JSON errors explicitly |
| Mutable default argument | Bug | `batch_log=[]` could share data across calls | Changed the default to `None` and initialized a list inside the function |
| Unused import | Code quality | The `os` module was imported but never used | Removed the unused import |
| File handling | Code quality | Files were opened without explicit encoding or context managers | Used `with open(..., encoding="utf-8")` |
| Missing docstrings | Maintainability | Module and functions lacked documentation | Added module and function docstrings |
| Naming and formatting | Style | Function naming, spacing and line lengths violated conventions | Used snake_case names and corrected formatting |
| Negative stock quantity | Data quality | Ibuprofen stock was initialized with a negative quantity | Corrected the sample stock adjustment to 15 units |

## Static Analysis Results

- **Pylint before:** 6.90/10
- **Pylint after:** 10.00/10
- **Bandit before:** 1 medium-severity and 1 low-severity finding
- **Bandit after:** No issues identified
- **Flake8 before:** Multiple formatting and code-style violations
- **Flake8 after:** No violations reported
