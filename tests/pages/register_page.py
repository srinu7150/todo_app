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
    CONFIRM_PASSWORD_INPUT = "input[name='confirm_password']"
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
    
    def fill_confirm_password(self, password: str) -> None:
        """
        Fill the confirm password field.
        
        Args:
            password: Password to confirm
        """
        self.fill_input("confirm_password", password)
    
    def click_register_button(self) -> None:
        """Click the register button."""
        self.click_button("Register")
    
    def submit_registration(
        self, 
        username: str, 
        email: str, 
        password: str,
        confirm_password: str = None
    ) -> None:
        """
        Fill all fields and click register.
        
        Args:
            username: Username to enter
            email: Email address to enter
            password: Password to enter
            confirm_password: Password to confirm (defaults to password)
        """
        if confirm_password is None:
            confirm_password = password
        
        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)
        self.fill_confirm_password(confirm_password)
        self.click_register_button()
    
    def wait_for_flash_message(self) -> Locator:
        """Wait for flash message to appear."""
        return self.wait_for_flash_message()
    
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return self.get_flash_message()
