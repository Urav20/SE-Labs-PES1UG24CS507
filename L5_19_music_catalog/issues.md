# Lab 5: Static Code Analysis — Issue Log


## 2. Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Missing module docstring | Code Quality | 1 | The Python file does not have a module-level docstring explaining its purpose. | Add a docstring at the beginning of the file. |
| Missing function docstrings | Code Quality | 9, 15, 20, 28, 32, 36, 43 | Functions do not have docstrings explaining their purpose. | Add suitable docstrings to all functions. |
| Invalid function naming | Code Quality | 9, 15, 28, 32, 36 | Function names such as `addSong` and `shufflePick` do not follow Python's snake_case naming convention. | Rename functions using snake_case and update their calls. |
| Mutable default argument | Bug / Code Quality | 9 | The function uses `playlist=[]` as a default argument, which can cause the same list to be reused across calls. | Change the default to `None` and initialize a new list inside the function. |
| SQL injection risk | Security | 10 | SQL is constructed using string formatting, which can cause incorrect queries and expose the application to SQL injection. | Use parameterized SQL queries with placeholders. |
| Unsafe pickle usage | Security | 1, 33 | The program uses `pickle` for serialization and deserialization. Loading untrusted pickle data can execute malicious code. | Replace pickle serialization and deserialization with JSON for the playlist data. |
| Random selection warning | Security Analysis | 17 | Bandit reports that `random.choice()` is not suitable for cryptographic purposes. | Review the use case. Ordinary random selection is appropriate for choosing a song, as cryptographic randomness is not required. |
| Unnecessary else statement | Code Quality | 22 | An `else` statement follows a branch that already returns a value. | Remove the unnecessary `else` and simplify the function. |
| Bare exception handler | Bug / Code Quality | 39 | A bare `except:` catches all exceptions and can hide unexpected errors. | Catch the appropriate exception explicitly. |
| Line too long | Formatting | 6, 10, 21, 49 | Some lines exceed the configured maximum line length. | Split long statements across multiple lines. |
| Multiple statements on one line | Formatting | 48 | The program contains more than one statement on the same line. | Place each statement on a separate line. |
| Ambiguous variable name | Code Quality / Formatting | 47 | The variable `l` is difficult to distinguish from the number `1`. | Rename it to `loaded_playlist` or another descriptive name. |
| Old-style string formatting | Code Quality | 10 | Pylint recommends a more appropriate string formatting approach. | Use parameterized SQL rather than formatting user values directly into the SQL statement. |

## 3. Static Analysis Tools Used

1. **Pylint:** Used to identify programming practice, naming, documentation, and code quality issues. Initial score: 4.57/10.
2. **Bandit:** Used to identify potentially insecure Python coding patterns. Initial findings: 4 issues, including 2 low-severity and 2 medium-severity findings.
3. **Flake8:** Used to identify formatting and style violations. Initial findings: 7 issues.

## 4. Fixing and Verification Plan

The identified issues will be fixed in stages. Security issues, particularly SQL query construction and unsafe deserialization, will be addressed first. The mutable default argument, exception handling, function naming, documentation, and formatting issues will then be corrected.

After making the changes, all three static analysis tools will be executed again. The updated reports will be compared with the original reports to verify that the issues have been resolved, all Flake8 formatting findings have been handled, and the Pylint score exceeds 9.5/10.

The program will also be executed to check that the original music catalog and playlist functionality continues to work.

## 5. Final Results

To be completed after implementing and verifying the fixes.

- Final Pylint score: Pending
- Remaining Bandit findings: Pending
- Remaining Flake8 findings: Pending
- Program execution test: Pending