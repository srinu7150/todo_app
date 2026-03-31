"""
Playwright Configuration for Flask Todo App Testing
====================================================
This configuration sets up Playwright for testing the Flask web application.
"""

from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config: Dict[str, Any] = {
    # Run tests in headless mode (no visible browser)
    "headless": True,
    
    # Base URL for the Flask app
    "base_url": "http://localhost:5000",
    
    # Timeout settings (in milliseconds)
    "timeout": 30000,
    "action_timeout": 10000,
    
    # Expect locator to be visible within this timeout
    "expect": {
        "timeout": 5000
    },
    
    # Maximum time each test can run before failing
    "max_timeout": 60000,
    
    # Use Chrome (your existing installation)
    "browser_name": "chrome",
    
    # Disable video recording to save disk space (enable with --video="on-first-fail" if needed)
    "video": "off",
    
    # Take screenshots on failure for debugging
    "screenshot": "only-on-failure",
    
    # Trace file for debugging failures (can be enabled with --trace="on-first-retry")
    "trace": "off",
    
    # Ignore HTTP errors (useful for testing redirects)
    "ignore_http_codes": [301, 302, 304],
    
    # Optimize test runs by running in parallel
    "workers": 1,  # Set to auto for parallel execution
    
    # Run tests in slow mode during development
    "slow_mo": 500,
    
    # Project configurations for different test suites
    "projects": [
        {
            "name": "chromium",
            "use": {
                "browserName": "chromium",
                "channel": "chrome-stable",  # Use Chrome for better compatibility
                "headless": True  # Ensure headless mode for all projects
            }
        },
        {
            "name": "firefox",
            "use": {
                "browserName": "firefox",
                "headless": True  # Ensure headless mode for all projects
            }
        },
        {
            "name": "webkit",
            "use": {
                "browserName": "webkit",
                "headless": True  # Ensure headless mode for all projects
            }
        }
    ],
    
    # Configure test directories
    "test_dir": "tests",
    
    # Filter patterns for tests to run
    "filter": None,
    
    # Reporter configuration
    "reporter": [
        ["list"],  # Simple console output
        ["html", {
            "outputFolder": "playwright-report",
            "open": "never"  # Don't auto-open HTML report
        }]
    ],
    
    # Environment variables to set for tests (read from .env file)
    "env": {
        "FLASK_ENV": "testing",
        "SQLALCHEMY_DATABASE_URI": os.getenv(
            "TEST_DATABASE_URL",
            f"postgresql://{os.getenv('TEST_DATABASE_USER', 'admin')}:{os.getenv('TEST_DATABASE_PASSWORD', 'admin123')}@localhost:5432/{os.getenv('TEST_DATABASE_NAME', 'todo_db_test')}"
        )
    }
}
