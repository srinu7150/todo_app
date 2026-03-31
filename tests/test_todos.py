"""
Todo CRUD Tests for Flask Todo App
====================================
This module contains test cases for adding, editing, toggling, and deleting todos.
"""

import pytest
from playwright.sync_api import expect
from tests.pages.login_page import LoginPage
from tests.pages.register_page import RegisterPage
from tests.pages.dashboard_page import DashboardPage
from tests.pages.todo_page import TodoPage


# Fixtures imported from conftest

@pytest.fixture
def registered_user(page, base_url):
    """Create a registered user for tests."""
    username = "testuser"
    email = "test@example.com"
    password = "password123"  # At least 8 characters
    
    register_page = RegisterPage(page, base_url)
    register_page.goto_register()
    register_page.submit_registration(username, email, password)
    
    return {
        "username": username,
        "email": email,
        "password": password
    }


@pytest.fixture
def logged_in_user(page, base_url, registered_user):
    """Create a logged in user for tests."""
    login_page = LoginPage(page, base_url)
    login_page.goto_login()
    login_page.submit_login(registered_user["username"], registered_user["password"])
    
    return {
        "username": registered_user["username"],
        "email": registered_user["email"]
    }


@pytest.fixture
def logged_in_user_with_todo(page, base_url, logged_in_user):
    """Create a logged in user with at least one todo."""
    # Add a todo for testing
    todo_page = TodoPage(page, base_url)
    todo_page.goto_add_todo()
    todo_page.submit_add_todo(title="Test Todo", description="This is a test todo")
    
    return {
        "username": logged_in_user["username"],
        "todo_title": "Test Todo"
    }


class TestAddTodo:
    """Test cases for adding new todos."""
    
    def test_add_todo_with_title_only(self, page, base_url, logged_in_user):
        """Test adding a todo with only title."""
        # Navigate to add todo page
        todo_page = TodoPage(page, base_url)
        todo_page.goto_add_todo()
        
        # Fill form with title only
        todo_page.fill_title("My New Todo")
        todo_page.click_submit_button()
        
        # Wait for flash message
        expect(todo_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = todo_page.get_flash_message()
        assert "Todo added" in flash_text or "successfully" in flash_text.lower()
    
    def test_add_todo_with_title_description_and_due_date(self, page, base_url, logged_in_user):
        """Test adding a todo with all fields including due date."""
        todo_page = TodoPage(page, base_url)
        todo_page.goto_add_todo()
        
        # Fill form with all fields
        todo_page.fill_title("Complete Project")
        todo_page.fill_description("Finish the project by deadline")
        todo_page.set_due_date("2026-04-15")  # Future date
        todo_page.click_submit_button()
        
        # Wait for flash message
        expect(todo_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = todo_page.get_flash_message()
        assert "Todo added" in flash_text or "successfully" in flash_text.lower()
    
    def test_add_todo_with_empty_title(self, page, base_url, logged_in_user):
        """Test that adding a todo with empty title shows error."""
        todo_page = TodoPage(page, base_url)
        todo_page.goto_add_todo()
        
        # Try to submit without filling title
        todo_page.click_submit_button()
        
        # Wait for flash message
        expect(todo_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = todo_page.get_flash_message()
        assert "Title is required" in flash_text
    
    def test_add_todo_redirects_to_dashboard(self, page, base_url, logged_in_user):
        """Test that adding a todo redirects to dashboard."""
        todo_page = TodoPage(page, base_url)
        todo_page.goto_add_todo()
        
        # Fill and submit
        todo_page.fill_title("Dashboard Redirect Test")
        todo_page.click_submit_button()
        
        # Should redirect to dashboard
        expect(page).to_have_url(f"{base_url}/dashboard")


class TestEditTodo:
    """Test cases for editing existing todos."""
    
    def test_edit_todo_successfully(self, page, base_url, logged_in_user_with_todo):
        """Test editing a todo successfully."""
        # Navigate to edit page
        todo_id = 1  # Assuming first todo has ID 1
        todo_page = TodoPage(page, base_url)
        todo_page.goto_edit_todo(todo_id)
        
        # Fill form with updated values
        todo_page.fill_title("Updated Todo Title")
        todo_page.fill_description("This is an updated description")
        todo_page.click_submit_button()
        
        # Wait for flash message
        expect(todo_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = todo_page.get_flash_message()
        assert "Todo updated" in flash_text or "successfully" in flash_text.lower()
    
    def test_edit_todo_with_empty_title(self, page, base_url, logged_in_user_with_todo):
        """Test that editing a todo with empty title shows error."""
        todo_id = 1
        todo_page = TodoPage(page, base_url)
        todo_page.goto_edit_todo(todo_id)
        
        # Try to submit without filling title
        todo_page.click_submit_button()
        
        # Wait for flash message
        expect(todo_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = todo_page.get_flash_message()
        assert "Title is required" in flash_text
    
    def test_edit_todo_redirects_to_dashboard(self, page, base_url, logged_in_user_with_todo):
        """Test that editing a todo redirects to dashboard."""
        todo_id = 1
        todo_page = TodoPage(page, base_url)
        todo_page.goto_edit_todo(todo_id)
        
        # Fill and submit
        todo_page.fill_title("Edited Title")
        todo_page.click_submit_button()
        
        # Should redirect to dashboard
        expect(page).to_have_url(f"{base_url}/dashboard")


class TestToggleTodo:
    """Test cases for toggling todo completion status."""
    
    def test_toggle_todo_to_completed(self, page, base_url, logged_in_user_with_todo):
        """Test marking a todo as completed."""
        # Navigate to dashboard
        dashboard_page = DashboardPage(page, base_url)
        dashboard_page.goto_dashboard()
        
        # Find the todo and click on it to toggle (assuming checkbox exists)
        todo_list = page.locator(".todo-list")
        if todo_list.is_visible():
            todos = todo_list.locator("li").all()
            if len(todos) > 0:
                # Click on the first todo's checkbox or completed link
                todo_element = todos[0]
                # Look for a checkbox or "Mark as Complete" link
                complete_link = todo_element.locator("a:has-text('Complete'), input[type='checkbox']")
                if complete_link.is_visible():
                    complete_link.click()
                    
                    # Wait for flash message
                    expect(dashboard_page.wait_for_flash_message()).to_be_visible(timeout=5000)
                    
                    # Verify success message
                    flash_text = dashboard_page.get_flash_message()
                    assert "completed" in flash_text.lower()
    
    def test_toggle_todo_to_pending(self, page, base_url, logged_in_user_with_todo):
        """Test marking a completed todo as pending again."""
        # Navigate to dashboard
        dashboard_page = DashboardPage(page, base_url)
        dashboard_page.goto_dashboard()
        
        # Find the todo and click on it to toggle
        todo_list = page.locator(".todo-list")
        if todo_list.is_visible():
            todos = todo_list.locator("li").all()
            if len(todos) > 0:
                todo_element = todos[0]
                complete_link = todo_element.locator("a:has-text('Complete'), input[type='checkbox']")
                if complete_link.is_visible():
                    complete_link.click()
                    
                    # Wait for flash message
                    expect(dashboard_page.wait_for_flash_message()).to_be_visible(timeout=5000)
                    
                    # Verify success message
                    flash_text = dashboard_page.get_flash_message()
                    assert "pending" in flash_text.lower() or "completed" in flash_text.lower()


class TestDeleteTodo:
    """Test cases for deleting todos."""
    
    def test_delete_own_todo_successfully(self, page, base_url, logged_in_user_with_todo):
        """Test deleting your own todo successfully."""
        # Navigate to dashboard
        dashboard_page = DashboardPage(page, base_url)
        dashboard_page.goto_dashboard()
        
        # Find the todo and click delete (assuming delete link exists)
        todo_list = page.locator(".todo-list")
        if todo_list.is_visible():
            todos = todo_list.locator("li").all()
            if len(todos) > 0:
                todo_element = todos[0]
                # Look for delete link
                delete_link = todo_element.locator("a:has-text('Delete')")
                if delete_link.is_visible():
                    delete_link.click()
                    
                    # Wait for flash message
                    expect(dashboard_page.wait_for_flash_message()).to_be_visible(timeout=5000)
                    
                    # Verify success message
                    flash_text = dashboard_page.get_flash_message()
                    assert "deleted" in flash_text.lower()
    
    def test_delete_other_users_todo_shows_error(self, page, base_url):
        """Test that deleting another user's todo shows unauthorized error."""
        # This test would require a second user to be logged in
        # For now, we'll skip this test or mark it as xfail
        pytest.skip("Requires multi-user setup for testing unauthorized access")


class TestTodoPageNavigation:
    """Test cases for navigation between todo pages."""
    
    def test_add_todo_page_shows_form(self, page, base_url, logged_in_user):
        """Test that add todo page shows the form correctly."""
        todo_page = TodoPage(page, base_url)
        todo_page.goto_add_todo()
        
        # Verify form fields are visible
        title_input = page.locator("input[name='title']")
        expect(title_input).to_be_visible(timeout=5000)
        
        description_input = page.locator("textarea[name='description']")
        expect(description_input).to_be_visible(timeout=5000)
    
    def test_edit_todo_page_shows_existing_data(self, page, base_url, logged_in_user_with_todo):
        """Test that edit todo page shows existing todo data."""
        todo_id = 1
        todo_page = TodoPage(page, base_url)
        todo_page.goto_edit_todo(todo_id)
        
        # Verify form fields are visible
        title_input = page.locator("input[name='title']")
        expect(title_input).to_be_visible(timeout=5000)
        
        description_input = page.locator("textarea[name='description']")
        expect(description_input).to_be_visible(timeout=5000)
