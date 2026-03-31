"""
LoginPage Page Object Model
===========================
This module provides a Page Object Model class for the login page of the Flask Todo App.
"""

from playwright.sync_api import Locator
from .base import BasePage


class LoginPage(BasePage):
    """
    Page Object Model for the Login Page.
    
    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Flask application
    """
    
    # Selectors
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit'], input[type='submit']:has-text('Login')"
    REGISTER_LINK = "a:has-text('Register')"
    FLASH_MESSAGES = ".alert"
    
    def __init__(self, page, base_url: str):
        """
        Initialize the LoginPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the Flask application
        """
        super().__init__(page, base_url)
    
    def goto_login(self) -> None:
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}/login")
    
    def fill_username(self, username: str) -> None:
        """
        Fill the username field.
        
        Args:
            username: Username to enter
        """
        self.fill_input("username", username)
    
    def fill_password(self, password: str) -> None:
        """
        Fill the password field.
        
        Args:
            password: Password to enter
        """
        self.fill_input("password", password)
    
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click_button("Login")
    
    def submit_login(self, username: str, password: str) -> None:
        """
        Fill username, password and click login.
        
        Args:
            username: Username to enter
            password: Password to enter
        """
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()
    
    def wait_for_flash_message(self) -> Locator:
        """Wait for flash message to appear."""
        return self.wait_for_flash_message()
    
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return self.get_flash_message()
    
    def navigate_to_register(self) -> None:
        """Navigate to the register page."""
        self.page.goto(f"{self.base_url}/register")
