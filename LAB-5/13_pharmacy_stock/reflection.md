# Lab 5 – Reflection

### 1. What is static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, code-quality problems and style violations.

### 2. What is the difference between Pylint, Bandit and Flake8?

Pylint checks code quality, possible logical errors and maintainability. Bandit identifies common security vulnerabilities in Python code. Flake8 checks formatting, whitespace and compliance with Python style conventions.

### 3. What issues were identified and fixed?

The tools identified a potential SQL injection vulnerability, overly broad exception handling, a mutable default argument, an unused import, missing documentation and formatting violations. The code was updated to address these findings.

### 4. How does static analysis improve software quality?

Static analysis helps developers identify problems early, improve security, maintain consistent coding standards and make programs easier to understand and maintain. It complements testing because it can detect certain issues without running the program.
