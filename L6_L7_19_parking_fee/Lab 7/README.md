# Lab 7 – Fuzz Testing: Parking Fee Application

This folder completes the Lab 7 fuzz-testing exercise using the parking-fee application from Lab 6. The three functions tested are `parking_fee()`, `find_slot()`, and `monthly_pass()`.

## 1. Setup

Use Python 3.8 or newer and install the required libraries:

```bash
python -m pip install hypothesis
python -m pip install pytest
```

## 2. Files

- `processor.py` – fixed application with input validation and a small runnable demonstration.
- `processor_buggy.py` – original Lab 6 logic, retained so the before-fix stage can be reproduced.
- `test_processor.py` – Hypothesis tests for all three functions.
- `requirements.txt` – required Python test dependencies.

## 3. Reproduce the lab in the required order

Run these commands from this `Lab 7` directory.

### Step 1 – Show the original buggy application

```bash
cp processor_buggy.py processor.py
python processor.py
```

Take Screenshot 1 showing the original application output.

### Step 2 – Run Hypothesis against the original code

```bash
python -m pytest -v test_processor.py
```

The tests are expected to find input-validation failures in the original implementation. Take Screenshot 2 showing the failing tests and Hypothesis examples.

### Step 3 – Restore the fixed application

Because the fixed `processor.py` is committed to this branch, restore it with:

```bash
git restore processor.py
python processor.py
```

Take Screenshot 3 showing the fixed application output.

### Step 4 – Run the tests against the fixed code

```bash
python -m pytest -v test_processor.py
```

Take Screenshot 4 showing the passing tests.

## 4. What the tests check

Hypothesis generates many values, including boundary values and unexpected data types. The tests check that:

- Valid parking-fee inputs produce non-negative fees.
- Stays of 30 minutes or less remain free.
- A lost ticket adds exactly 200 to the fee.
- Increasing the duration never decreases the fee.
- Invalid vehicle names, durations, slot counts, and flag values are rejected cleanly.
- Slot allocation returns one of the supported locations.
- Monthly passes are non-negative and residents receive the 20% discount.

The original Lab 6 directory is left unchanged.

## 5. Lab 7 deliverables

1. A PDF containing the four terminal screenshots listed above.
2. The fixed `processor.py` application.
3. The completed `test_processor.py` Hypothesis test file.

The screenshots must be captured from your own terminal after running the commands. They are not fabricated or pre-filled in this repository.
