# Lab 6 — Code and Branch Coverage

This folder adapts the SETAPESU26 pet-walking service reference application for the Lab 6 submission.

## Files

- `pet_walking_service.py` — original application under test from the reference repository.
- `test_pet_walking.py` — original starter test from the reference repository.
- `CodeCoverageTest_PES1UG24CS200_application.py` — expanded tests for line/code coverage.
- `BranchCoverageTest_PES1UG24CS200_application.py` — tests designed to exercise both outcomes of decision branches.

## Setup

Run these commands from this folder:

```bash
python -m pip install pytest coverage
```

## Code coverage

```bash
coverage erase
coverage run --source=pet_walking_service -m pytest -v CodeCoverageTest_PES1UG24CS200_application.py
coverage report -m
```

## Branch coverage

```bash
coverage erase
coverage run --branch --source=pet_walking_service -m pytest -v BranchCoverageTest_PES1UG24CS200_application.py
coverage report -m
```

`coverage report -m` displays missing line numbers. With `--branch`, it also reports branch counts and partial branches.

## Reference baseline

The original single starter test was measured against the application before adding the expanded tests:
- Line coverage: 47%
- Branch coverage: 43%

The expanded code-coverage test file was validated at 100% line coverage (17 tests).
The expanded branch-coverage test file was validated at 100% combined coverage (23 tests, 40/40 branches).

Re-run the commands on your machine and capture your own terminal screenshots for submission.
