# Playwright Test Suite for Flask Todo App

This directory contains comprehensive Playwright test cases for the Flask Todo Application.

## Project Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Fixtures and setup/teardown
└── pages/                   # Page Object Models
    ├── __init__.py
    ├── base.py              # Base page class with common methods
    ├── login_page.py        # LoginPage POM
    ├── register_page.py     # RegisterPage POM
    ├── dashboard_page.py    # DashboardPage POM
    └── todo_page.py         # TodoPage POM (Add/Edit)

test_auth.py                 # Authentication tests (register, login, logout)
test_todos.py                # Todo CRUD tests (add, edit, toggle, delete)
```

## Test Coverage

### Authentication Tests (`test_auth.py`)
- **Registration**
  - Successful user registration with valid credentials
  - Registration validation errors (short username, invalid email, short password)
  - Duplicate username/email handling

- **Login**
  - Successful login with valid credentials
  - Login with invalid credentials
  - Auto-redirect to dashboard after successful login
  - Login with email as username

- **Logout**
  - Successful logout
  - Redirect to login page after logout
  - Flash message verification

### Todo CRUD Tests (`test_todos.py`)
- **Add Todo**
  - Successfully add a new todo with title only
  - Add todo with title, description, and due date
  - Validation: empty title error
  - Redirect to dashboard after successful add

- **Edit Todo**
  - Edit existing todo (title, description, due date)
  - Toggle completed status
  - Validation: empty title error
  - Unauthorized edit attempt handling

- **Toggle Todo**
  - Mark todo as completed
  - Mark todo as pending
  - Flash message verification

- **Delete Todo**
  - Delete own todo successfully
  - Unauthorized delete attempt (403 response)

## Setup Instructions

### 1. Install Playwright and Browsers

```bash
# Install Playwright core
pip install playwright

# Install browsers (Chromium recommended for Flask apps)
playwright install chromium
# Optional: Install other browsers
playwright install firefox
playwright install webkit
```

### 2. Ensure Flask App is Running

The tests expect the Flask app to be running at `http://localhost:5000`.

Start the Flask app:

```bash
cd /home/srinu/repos/python/todo_app
source venv/bin/activate
python app/flask_app.py &
```

### 3. Install Test Dependencies (Optional)

If you want to use pytest with rich reporting:

```bash
pip install pytest pytest-xdist
```

## Running Tests

### Run All Tests

```bash
cd /home/srinu/repos/python/todo_app
python -m pytest tests/ -v
```

### Run Specific Test File

```bash
# Run only authentication tests
python -m pytest tests/test_auth.py -v

# Run only todo tests
python -m pytest tests/test_todos.py -v
```

### Run with Headed Browser (for debugging)

```bash
python -m pytest tests/ -v --headed
```

### Run Specific Test Class

```bash
# Run only registration tests
python -m pytest tests/test_auth.py::TestRegistration -v

# Run only login tests
python -m pytest tests/test_auth.py::TestLogin -v
```

### Run with Screenshot on Failure

```bash
python -m pytest tests/ -v --screenshot=on-first-failure
```

### Run with Video Recording (for debugging failures)

```bash
python -m pytest tests/ -v --video=on-first-retry
```

### Run Specific Project/Browser

```bash
# Run only on Chromium
python -m pytest tests/ -v --project=chromium

# Run on all browsers in parallel
python -m pytest tests/ -v --project=chromium,firefox,webkit
```

## Test Fixtures

The test suite uses the following fixtures defined in `conftest.py`:

| Fixture | Description |
|---------|-------------|
| `browser` | Browser instance for the test session |
| `context` | Fresh browser context for each test |
| `page` | Fresh page for each test |
| `base_url` | Base URL of the Flask app (`http://localhost:5000`) |
| `login_page` | LoginPage POM instance |
| `register_page` | RegisterPage POM instance |
| `dashboard_page` | DashboardPage POM instance |
| `todo_page` | TodoPage POM instance |
| `registered_user` | Creates a registered user for tests |
| `logged_in_user` | Creates a logged in user for tests |
| `logged_in_user_with_todo` | Creates a logged in user with at least one todo |

## Page Object Models

The Page Object Model (POM) pattern is used to separate page interactions from test logic.

### BasePage (`pages/base.py`)
Common methods available to all page objects:
- `_get_locator(selector)` - Get a locator with default timeout
- `wait_for_url_to_contain(substring)` - Wait for URL to contain substring
- `wait_for_flash_message(message=None)` - Wait for flash message
- `get_flash_message()` - Get flash message text
- `click_button(button_text)` - Click button by visible text
- `fill_input(input_name_or_id, value)` - Fill input field
- `get_input_value(input_name_or_id)` - Get input field value

### LoginPage (`pages/login_page.py`)
Methods:
- `goto_login()` - Navigate to login page
- `fill_username(username)` - Fill username field
- `fill_password(password)` - Fill password field
- `click_login_button()` - Click login button
- `submit_login(username, password)` - Fill and submit login form
- `navigate_to_register()` - Navigate to register page

### RegisterPage (`pages/register_page.py`)
Methods:
- `goto_register()` - Navigate to register page
- `fill_username(username)` - Fill username field
- `fill_email(email)` - Fill email field
- `fill_password(password)` - Fill password field
- `fill_confirm_password(password)` - Fill confirm password field
- `click_register_button()` - Click register button
- `submit_registration(username, email, password, confirm_password=None)` - Fill and submit registration form

### DashboardPage (`pages/dashboard_page.py`)
Methods:
- `goto_dashboard()` - Navigate to dashboard page
- `wait_for_todos_to_load()` - Wait for todos to load
- `get_todo_count()` - Get total number of todos
- `get_completed_count()` - Get number of completed todos
- `get_pending_count()` - Get number of pending todos
- `get_todo_by_title(title)` - Get todo element by title
- `click_add_todo_button()` - Click Add Todo button
- `navigate_to_stats()` - Navigate to stats page

### TodoPage (`pages/todo_page.py`)
Methods:
- `goto_add_todo()` - Navigate to add todo page
- `goto_edit_todo(todo_id)` - Navigate to edit todo page
- `fill_title(title)` - Fill title field
- `fill_description(description)` - Fill description field
- `set_due_date(due_date)` - Set due date
- `click_submit_button()` - Click submit button
- `click_cancel_button()` - Click cancel button
- `submit_add_todo(title, description="", due_date="")` - Fill and submit add form
- `submit_edit_todo(title, description="", due_date="")` - Fill and submit edit form

## Configuration

The Playwright configuration is in `playwright.config.py`. Key settings:

| Setting | Value | Description |
|---------|-------|-------------|
| `headless` | `True` | Run browser without UI (use `--headed` to disable) |
| `base_url` | `http://localhost:5000` | Base URL of Flask app |
| `timeout` | `30000` | Default timeout in ms |
| `screenshot` | `only-on-failure` | Take screenshots on test failures |
| `video` | `off` | Don't record videos (use `--video=on-first-fail` if needed) |
| `slow_mo` | `500` | Slow down tests by 500ms for debugging |

## Environment Variables

The tests use these environment variables:

```bash
FLASK_ENV=testing
SQLALCHEMY_DATABASE_URI=postgresql://admin:admin123@localhost:5432/todo_db_test
```

These are set in `playwright.config.py` but can be overridden via command line:

```bash
FLASK_ENV=testing SQLALCHEMY_DATABASE_URI=... pytest tests/
```

## Test Isolation

Each test function runs in isolation with:
- Fresh browser context
- Clean page state
- Database cleanup after each test (via `cleanup_database` fixture)

Note: The database cleanup assumes the Flask app is running and accessible. For production use, consider using a separate test database.

## Troubleshooting

### Tests Fail to Connect to Flask App

Make sure the Flask app is running:

```bash
python app/flask_app.py &
```

Check that it's accessible at `http://localhost:5000`.

### Tests Timeout

Increase timeouts in `playwright.config.py` or use `--timeout` flag:

```bash
python -m pytest tests/ --timeout=60000
```

### Debug Test Failures

Run with headed browser and slow motion:

```bash
python -m pytest tests/test_auth.py::TestLogin::test_successful_login -v --headed --slowmo=2000
```

### View Screenshots on Failure

Screenshots are saved in the `tests/` directory when a test fails.

### Generate HTML Report

```bash
python -m pytest tests/ --reporter=html --reporter-html-report=playwright-report.html
```

## Adding New Tests

1. Create a new test file in `tests/` (e.g., `test_stats.py`)
2. Use existing fixtures from `conftest.py`
3. Use Page Object Models from `tests/pages/`
4. Follow the naming convention: `test_<feature>_<scenario>`
5. Add tests to appropriate test class

Example:

```python
# tests/test_stats.py
def test_stats_page_shows_correct_counts(page, base_url, logged_in_user_with_todo):
    """Test that stats page shows correct todo counts."""
    # Test implementation
    pass
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install playwright pytest
      - name: Install Playwright browsers
        run: npx playwright install chromium
      - name: Run tests
        run: python -m pytest tests/ -v
```

## License

This test suite is provided as part of the Flask Todo App project.
