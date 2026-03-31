"""
RegisterPage Page Object Model
==============================
This module provides a Page Object Model class for the registration page of the Flask Todo App.
"""

from playwright.sync_api import Locator
from .base import BasePage


class RegisterPage(BasePage):
    """
    Page Object Model for the Registration Page.
    
    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Flask application
    """
    
    # Selectors
    USERNAME_INPUT = "input[name='username']"
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    REGISTER_BUTTON = "button[type='submit'], input[type='submit']:has-text('Register')"
    FLASH_MESSAGES = ".alert"
    
    def __init__(self, page, base_url: str):
        """
        Initialize the RegisterPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the Flask application
        """
        super().__init__(page, base_url)
    
    def goto_register(self) -> None:
        """Navigate to the registration page."""
        self.page.goto(f"{self.base_url}/register")
    
    def fill_username(self, username: str) -> None:
        """
        Fill the username field.
        
        Args:
            username: Username to enter
        """
        self.fill_input("username", username)
    
    def fill_email(self, email: str) -> None:
        """
        Fill the email field.
        
        Args:
            email: Email address to enter
        """
        self.fill_input("email", email)
    
    def fill_password(self, password: str) -> None:
        """
        Fill the password field.
        
        Args:
            password: Password to enter
        """
        self.fill_input("password", password)
    
    # Note: The register form does NOT have a confirm_password field
    # Only username, email, and password are required
    
    def click_register_button(self) -> None:
        """Click the register button."""
        self.click_button("Register")
    
    def submit_registration(
        self,
        username: str,
        email: str,
        password: str
    ) -> None:
        """
        Fill all fields and click register.
        
        Args:
            username: Username to enter
            email: Email address to enter
            password: Password to enter
        """
        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)
        self.click_register_button()
    
    def wait_for_flash_message(self, message: str = None) -> Locator:
        """Wait for flash message to appear."""
        return super().wait_for_flash_message(message)
    
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return super().get_flash_message()
