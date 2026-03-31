"""
TodoPage Page Object Model
==========================
This module provides a Page Object Model class for the Add/Edit Todo pages of the Flask Todo App.
"""

from playwright.sync_api import Locator
from .base import BasePage


class TodoPage(BasePage):
    """
    Page Object Model for Add/Edit Todo Pages.
    
    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Flask application
    """
    
    # Selectors
    ADD_TODO_URL = "/todo/add"
    EDIT_TODO_URL = "/todo/"
    TITLE_INPUT = "input[name='title']"
    DESCRIPTION_INPUT = "textarea[name='description']"
    DUE_DATE_INPUT = "input[name='due_date']"
    SUBMIT_BUTTON = "button[type='submit'], input[type='submit']:has-text('Add'), input[type='submit']:has-text('Update')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    FLASH_MESSAGES = ".alert"
    
    def __init__(self, page, base_url: str):
        """
        Initialize the TodoPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the Flask application
        """
        super().__init__(page, base_url)
    
    def goto_add_todo(self) -> None:
        """Navigate to the add todo page."""
        self.page.goto(f"{self.base_url}{self.ADD_TODO_URL}")
    
    def goto_edit_todo(self, todo_id: int) -> None:
        """
        Navigate to edit a specific todo.
        
        Args:
            todo_id: ID of the todo to edit
        """
        self.page.goto(f"{self.base_url}{self.EDIT_TODO_URL}{todo_id}")
    
    def fill_title(self, title: str) -> None:
        """
        Fill the title field.
        
        Args:
            title: Title of the todo
        """
        self.fill_input("title", title)
    
    def fill_description(self, description: str = "") -> None:
        """
        Fill the description field.
        
        Args:
            description: Description of the todo (can be empty string)
        """
        self.fill_input("description", description)
    
    def set_due_date(self, due_date: str) -> None:
        """
        Set the due date for the todo.
        
        Args:
            due_date: Due date in YYYY-MM-DD format or datetime-local value
        """
        self.fill_input("due_date", due_date)
    
    def click_submit_button(self) -> None:
        """Click the submit button (Add or Update)."""
        # Wait for form to be valid first
        title_input = self._get_locator(self.TITLE_INPUT)
        if not title_input.is_enabled():
            title_input.fill("", timeout=3000)
        
        self.click_button("Add") or self.click_button("Update")
    
    def click_cancel_button(self) -> None:
        """Click the cancel button."""
        self.click_button("Cancel")
    
    def submit_add_todo(
        self, 
        title: str, 
        description: str = "",
        due_date: str = ""
    ) -> None:
        """
        Fill all fields and submit a new todo.
        
        Args:
            title: Title of the todo
            description: Description of the todo (can be empty)
            due_date: Due date in YYYY-MM-DD format or datetime-local value
        """
        self.fill_title(title)
        self.fill_description(description)
        if due_date:
            self.set_due_date(due_date)
        self.click_submit_button()
    
    def submit_edit_todo(
        self, 
        title: str, 
        description: str = "",
        due_date: str = ""
    ) -> None:
        """
        Fill all fields and update a todo.
        
        Args:
            title: Title of the todo
            description: Description of the todo (can be empty)
            due_date: Due date in YYYY-MM-DD format or datetime-local value
        """
        self.fill_title(title)
        self.fill_description(description)
        if due_date:
            self.set_due_date(due_date)
        self.click_submit_button()
    
    def wait_for_flash_message(self, message: str = None) -> Locator:
        """Wait for flash message to appear."""
        return super().wait_for_flash_message(message)
    
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return super().get_flash_message()
