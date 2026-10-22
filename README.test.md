# Test Instructions — Data Issues Grid

Automated [Playwright](https://playwright.dev/python/) + [pytest](https://docs.pytest.org/) tests for the Active Prime Data Issues page.
All 5 tests live in [tests/test_data_issues.py](tests/test_data_issues.py).

## Prerequisites

### Python 3.12 install

Download and install Python 3.12 from https://www.python.org/downloads/ (or from the Microsoft Store).
Verify the installation:

```powershell
python --version   # should print Python 3.12.x
```

### Install Python dependencies

```powershell
python -m pip install -r tests/requirements.txt
```

### Install the Chromium browser for Playwright

```powershell
python -m playwright install chromium
```

## Running the tests

### Run them together

```powershell
python -m pytest tests/test_data_issues.py -v
```

### Run independently

```powershell
python -m pytest "tests/test_data_issues.py::test_navigate_to_data_issues_grid" -v
python -m pytest "tests/test_data_issues.py::test_all_original_rows_have_nonempty_sfid" -v
python -m pytest "tests/test_data_issues.py::test_select_original_value_for_seventh_card" -v
python -m pytest "tests/test_data_issues.py::test_edit_final_row_issue_field" -v
python -m pytest "tests/test_data_issues.py::test_checkbox_selection_counter" -v
```

You can also filter by keyword:

```powershell
python -m pytest tests/test_data_issues.py -k "checkbox" -v
```

## What each test covers

| # | Test | Verifies |
|---|------|----------|
| 1 | `test_navigate_to_data_issues_grid` | Data Issues page loads and displays 10 issue cards |
| 2 | `test_all_original_rows_have_nonempty_sfid` | Every card's original row contains a non-empty `sfid` |
| 3 | `test_select_original_value_for_seventh_card` | Selecting the original value via radio button updates the final row |
| 4 | `test_edit_final_row_issue_field` | Inline editing of the issue column in the final row |
| 5 | `test_checkbox_selection_counter` | Selection counter shows correct counts and hides when empty |

## How it works

- **No manual server needed.** The session fixture in [tests/conftest.py](tests/conftest.py) automatically starts a local HTTP server on port `8080` serving the [app](app) folder, and shuts it down when the run finishes. If something is already listening on port 8080, the fixture reuses it.
- The `issues_page` fixture opens `http://localhost:8080/index.html`, dismisses the welcome modal, steps through the two nested iframes (`#outerFrame` → `#appFrame`), clicks **Review & Fix Issues**, and waits for the 10 issue cards to render before each test runs.
- Tests run **headless** by default and are fully independent — each test gets a fresh page and fresh navigation, so any subset can run in any order.

## Useful options

```powershell
python -m pytest tests/test_data_issues.py -v -s        # show print output
python -m pytest tests/test_data_issues.py --tb=short   # shorter tracebacks
python -m pytest tests/test_data_issues.py -x           # stop on first failure
```

To watch the browser while tests run, change `headless=True` to `headless=False` in the `browser` fixture in [tests/conftest.py](tests/conftest.py).
