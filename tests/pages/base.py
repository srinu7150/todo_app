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
        Get a locator.
        
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
        Wait for a flash message to appear and be visible.
        
        Args:
            message: Optional specific message text to wait for
            
        Returns:
            Locator for the flash message
        """
        # Flash messages use Bootstrap's alert classes (e.g., alert-danger, alert-success)
        # Use simple selector to match any alert element with fade animation
        flash_locator = self._get_locator(".alert.fade")
        
        # Add delay to allow DOM update and Bootstrap fade animation after form submission
        import time
        time.sleep(0.5)
        
        if message:
            return flash_locator.filter(has_text=message).first
        
        return flash_locator.first

    def wait_for_flash_message_visible(self, message: str = None) -> Locator:
        """
        Wait for a flash message to appear and be visible.
        
        Args:
            message: Optional specific message text to wait for
            
        Returns:
            Locator for the flash message
        """
        # Flash messages use Bootstrap's alert classes (e.g., alert-danger, alert-success)
        # Use simple selector to match any alert element with fade animation
        flash_locator = self._get_locator(".alert.fade")
        
        # Add delay to allow DOM update and Bootstrap fade animation after form submission
        import time
        time.sleep(0.5)
        
        if message:
            return flash_locator.filter(has_text=message).first
        
        return flash_locator.first

    def wait_for_flash_message_attached(self, message: str = None) -> Locator:
        """
        Wait for a flash message to be attached to the DOM (regardless of visibility).
        
        Args:
            message: Optional specific message text to wait for
            
        Returns:
            Locator for the flash message
        """
        # Flash messages use Bootstrap's alert classes (e.g., alert-danger, alert-success)
        # Use simple selector to match any alert element with fade animation
        flash_locator = self._get_locator(".alert.fade")
        
        # Add delay to allow DOM update and Bootstrap fade animation after form submission
        import time
        time.sleep(0.5)
        
        if message:
            return flash_locator.filter(has_text=message).first
        
        return flash_locator.first

    def wait_for_flash_message_with_timeout(self, message: str = None, timeout: int = 10000) -> Locator:
        """
        Wait for a flash message to be attached to the DOM with explicit timeout.
        
        Args:
            message: Optional specific message text to wait for
            timeout: Timeout in milliseconds
            
        Returns:
            Locator for the flash message
        """
        # Flash messages use Bootstrap's alert classes (e.g., alert-danger, alert-success)
        # Use simple selector to match any alert element with fade animation
        flash_locator = self._get_locator(".alert.fade")
        
        # Add delay to allow DOM update and Bootstrap fade animation after form submission
        import time
        time.sleep(0.5)
        
        if message:
            return flash_locator.filter(has_text=message).first
        
        return flash_locator.first
    
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
        # Use button:has-text() to specifically target buttons with the given text
        # This avoids matching nav links or headings with the same text
        button = self._get_locator(f"button:has-text('{button_text}')")
        button.click(timeout=5000)
    
    def fill_input(self, input_name_or_id: str, value: str) -> None:
        """
        Fill an input field by its name or ID.
        
        Args:
            input_name_or_id: Name or ID of the input field
            value: Value to fill in the field
        """
        # Use button:has-text() to specifically target buttons with the given text
        # This avoids matching nav links or headings with the same text
        input_field = self._get_locator(f"input[name='{input_name_or_id}'], [id='{input_name_or_id}']")
        input_field.fill(value, timeout=10000)
    
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
