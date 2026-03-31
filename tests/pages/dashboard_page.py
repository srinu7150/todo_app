"""
DashboardPage Page Object Model
================================
This module provides a Page Object Model class for the dashboard page of the Flask Todo App.
"""

from playwright.sync_api import Locator
from .base import BasePage


class DashboardPage(BasePage):
    """
    Page Object Model for the Dashboard Page.
    
    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Flask application
    """
    
    # Selectors
    DASHBOARD_URL = "/dashboard"
    TODO_LIST = "ul.todo-list li"
    ADD_TODO_BUTTON = ".btn-primary:has-text('Add Todo'), a:has-text('Add Todo')"
    STATS_LINK = "a:has-text('Stats')"
    NAVIGATION_LINKS = "nav ul li a"
    
    def __init__(self, page, base_url: str):
        """
        Initialize the DashboardPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the Flask application
        """
        super().__init__(page, base_url)
    
    def goto_dashboard(self) -> None:
        """Navigate to the dashboard page."""
        self.page.goto(f"{self.base_url}{self.DASHBOARD_URL}")
    
    def wait_for_todos_to_load(self) -> None:
        """Wait for todos to load on the dashboard."""
        # Wait for todo list container to be visible
        self._get_locator(".todo-list").wait_for(state="visible", timeout=10000)
    
    def get_todo_count(self) -> int:
        """
        Get the total number of todos.
        
        Returns:
            Number of todos on the dashboard
        """
        todo_list = self._get_locator(".todo-list")
        return len(todo_list.locator("li").all())
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed todos.
        
        Returns:
            Number of completed todos
        """
        completed_todos = self._get_locator(".todo-list li.completed")
        return len(completed_todos.all())
    
    def get_pending_count(self) -> int:
        """
        Get the number of pending todos.
        
        Returns:
            Number of pending todos
        """
        pending_todos = self._get_locator(".todo-list li:not(.completed)")
        return len(pending_todos.all())
    
    def get_todo_by_title(self, title: str) -> Locator:
        """
        Get a todo element by its title.
        
        Args:
            title: Title of the todo
            
        Returns:
            Locator for the todo element
        """
        return self._get_locator(f"li:has-text('{title}')")
    
    def click_add_todo_button(self) -> None:
        """Click the 'Add Todo' button."""
        self.click_button("Add Todo")
    
    def navigate_to_stats(self) -> None:
        """Navigate to the stats page."""
        self.page.goto(f"{self.base_url}/stats")
    
    def get_navigation_links(self) -> list:
        """
        Get all navigation links.
        
        Returns:
            List of navigation link texts
        """
        links = self._get_locator(self.NAVIGATION_LINKS).all()
        return [link.inner_text().strip() for link in links]
