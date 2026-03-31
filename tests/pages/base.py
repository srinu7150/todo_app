"""
Base Page Class for Playwright Page Object Model
================================================
This module provides a base class for all page objects in the test suite.
"""

from playwright.sync_api import Page, Locator


class BasePage:
    """
    Base class for all page objects using Page Object Model pattern.
    
    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Flask application
    """
    
    def __init__(self, page: Page, base_url: str):
        """
        Initialize the base page object.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the Flask application
        """
        self.page = page
        self.base_url = base_url
    
    def _get_locator(self, selector: str) -> Locator:
        """
        Get a locator with default timeout.
        
        Args:
            selector: CSS or XPath selector
            
        Returns:
            Playwright Locator instance
        """
        return self.page.locator(selector)
    
    def wait_for_url_to_contain(self, substring: str) -> None:
        """
        Wait for the URL to contain a specific substring.
        
        Args:
            substring: URL substring to wait for
        """
        self.page.wait_for_url(lambda url: substring in url)
    
    def wait_for_flash_message(self, message: str = None) -> Locator:
        """
        Wait for a flash message to appear.
        
        Args:
            message: Optional specific message text to wait for
            
        Returns:
            Locator for the flash message
        """
        # Flash messages are typically in a notification container
        flash_locator = self._get_locator(".alert", timeout=5000)
        if message:
            return flash_locator.filter(has_text=message)
        return flash_locator
    
    def get_flash_message(self) -> str:
        """
        Get the text of the most recent flash message.
        
        Returns:
            Flash message text or empty string if no message found
        """
        flash = self.wait_for_flash_message()
        return flash.inner_text(timeout=3000).strip()
    
    def click_button(self, button_text: str) -> None:
        """
        Click a button by its visible text.
        
        Args:
            button_text: Text of the button to click
        """
        button = self._get_locator(f"text={button_text}")
        button.click(timeout=5000)
    
    def fill_input(self, input_name_or_id: str, value: str) -> None:
        """
        Fill an input field by its name or ID.
        
        Args:
            input_name_or_id: Name or ID of the input field
            value: Value to fill in the field
        """
        input_field = self._get_locator(f"input[name='{input_name_or_id}'], [id='{input_name_or_id}']")
        input_field.fill(value, timeout=5000)
    
    def get_input_value(self, input_name_or_id: str) -> str:
        """
        Get the value of an input field.
        
        Args:
            input_name_or_id: Name or ID of the input field
            
        Returns:
            Input field value
        """
        input_field = self._get_locator(f"input[name='{input_name_or_id}'], [id='{input_name_or_id}']")
        return input_field.input_value()
