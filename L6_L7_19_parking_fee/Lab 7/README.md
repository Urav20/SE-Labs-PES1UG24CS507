# Lab 7 – Fuzz Testing: Parking Fee Application

This folder applies the Lab 7 fuzz-testing exercise to the parking-fee application from Lab 6.

## Setup

Use Python 3.8 or newer.

```bash
python -m pip install hypothesis pytest
```

## Files

- `parking_fee.py`: the application with defensive input validation.
- `test_processor.py`: Hypothesis property-based tests for all three functions: `parking_fee`, `find_slot`, and `monthly_pass`.

## Run

Run the application:

```bash
python parking_fee.py
```

Run the fuzz tests:

```bash
python -m pytest -v test_processor.py
```

Hypothesis generates varied values (including unusual types and boundary values) and shrinks failures to small examples. The tests cover valid-input properties and rejection of invalid vehicle names, durations, slot counts, and flags.

## Lab 7 evidence

Capture your own terminal screenshots for:
1. The application output before fixing (use the original Lab 6 version of `parking_fee.py`).
2. Failing tests before fixes (run the test file against the original implementation).
3. The fixed application's output.
4. The passing tests after fixes.

The repository's original Lab 6 files are retained unchanged. This Lab 7 folder contains the fuzz-tested, hardened version.
