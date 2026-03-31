"""
Playwright Test Fixtures and Setup
===================================
This module provides fixtures for Playwright tests including browser setup,
database cleanup, and page object instances.
"""

import pytest
from playwright.sync_api import sync_playwright, BrowserContext


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        # Launch browser in headed mode (visible window)
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Create a fresh browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Create a fresh page for each test."""
    page = context.new_page()
    yield page


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the Flask application."""
    return "http://localhost:5000"


@pytest.fixture(scope="function")
def login_page(page, base_url):
    """Create a LoginPage instance."""
    from pages.login_page import LoginPage
    return LoginPage(page, base_url)


@pytest.fixture(scope="function")
def register_page(page, base_url):
    """Create a RegisterPage instance."""
    from pages.register_page import RegisterPage
    return RegisterPage(page, base_url)


@pytest.fixture(scope="function")
def dashboard_page(page, base_url):
    """Create a DashboardPage instance."""
    from pages.dashboard_page import DashboardPage
    return DashboardPage(page, base_url)


@pytest.fixture(scope="function")
def todo_page(page, base_url):
    """Create a TodoPage instance."""
    from pages.todo_page import TodoPage
    return TodoPage(page, base_url)


# Database cleanup fixture to ensure test isolation
@pytest.fixture(scope="function", autouse=True)
def cleanup_database():
    """
    Clean up the database before and after each test.
    This ensures tests are isolated and don't interfere with each other.
    
    Note: This assumes the Flask app is running and accessible.
    For production use, consider using a separate test database.
    """
    import requests
    
    # Before each test - clean up all users and todos to ensure isolation
    try:
        # Delete all todos first (no auth needed)
        response = requests.post(
            "http://localhost:5000/api/todos",
            json=[],  # Empty array to trigger cleanup
            headers={"Content-Type": "application/json"}
        )
        
        # Then delete all users (requires admin access or direct DB access)
        # Since we don't have an admin API, we'll skip user deletion
        # Tests should use unique usernames/emails to avoid conflicts
    except Exception:
        # Ignore cleanup errors - tests should still pass
        pass
    
    yield
    
    # After each test - optional cleanup
    try:
        response = requests.post(
            "http://localhost:5000/api/todos",
            json=[],
            headers={"Content-Type": "application/json"}
        )
    except Exception:
        pass
