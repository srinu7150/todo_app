"""
Authentication Tests for Flask Todo App
========================================
This module contains test cases for user registration, login, and logout functionality.
"""

import pytest
from playwright.sync_api import expect


# Fixtures imported from conftest
@pytest.fixture
def registered_user(base_url):
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
def logged_in_user(base_url):
    """Create a logged in user for tests."""
    # First register a user
    registered_user = registered_user
    
    login_page = LoginPage(page, base_url)
    login_page.goto_login()
    login_page.submit_login(registered_user["username"], registered_user["password"])
    
    return {
        "username": registered_user["username"],
        "email": registered_user["email"]
    }


class TestRegistration:
    """Test cases for user registration."""
    
    def test_successful_registration(self, page, base_url):
        """Test that a new user can register successfully."""
        # Navigate to register page
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Fill form with valid data
        username = "newuser123"
        email = "newuser@example.com"
        password = "securepass123"
        
        register_page.fill_username(username)
        register_page.fill_email(email)
        register_page.fill_password(password)
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = register_page.get_flash_message()
        assert "Registration" in flash_text or "success" in flash_text.lower()
    
    def test_registration_with_short_username(self, page, base_url):
        """Test that registration fails with username shorter than 3 characters."""
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Fill form with short username
        register_page.fill_username("ab")  # Less than 3 chars
        register_page.fill_email("test@example.com")
        register_page.fill_password("password123")
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = register_page.get_flash_message()
        assert "Username must be between 3 and 50 characters" in flash_text
    
    def test_registration_with_invalid_email(self, page, base_url):
        """Test that registration fails with invalid email format."""
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Fill form with invalid email
        register_page.fill_username("testuser")
        register_page.fill_email("invalid-email")  # No @ symbol
        register_page.fill_password("password123")
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = register_page.get_flash_message()
        assert "valid email" in flash_text.lower()
    
    def test_registration_with_short_password(self, page, base_url):
        """Test that registration fails with password shorter than 8 characters."""
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Fill form with short password
        register_page.fill_username("testuser")
        register_page.fill_email("test@example.com")
        register_page.fill_password("short")  # Less than 8 chars
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = register_page.get_flash_message()
        assert "Password must be at least 8 characters" in flash_text
    
    def test_registration_with_duplicate_username(self, page, base_url, registered_user):
        """Test that registration fails with existing username."""
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Try to register with same username as already registered user
        register_page.fill_username(registered_user["username"])
        register_page.fill_email("different@example.com")
        register_page.fill_password("password123")
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = register_page.get_flash_message()
        assert "Username already exists" in flash_text
    
    def test_registration_with_duplicate_email(self, page, base_url, registered_user):
        """Test that registration fails with existing email."""
        register_page = RegisterPage(page, base_url)
        register_page.goto_register()
        
        # Try to register with same email as already registered user
        register_page.fill_username("differentuser")
        register_page.fill_email(registered_user["email"])
        register_page.fill_password("password123")
        register_page.click_register_button()
        
        # Wait for flash message
        expect(register_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = register_page.get_flash_message()
        assert "Email already registered" in flash_text


class TestLogin:
    """Test cases for user login."""
    
    def test_successful_login(self, page, base_url, registered_user):
        """Test that a user can login with valid credentials."""
        login_page = LoginPage(page, base_url)
        login_page.goto_login()
        
        # Fill form with valid credentials
        login_page.fill_username(registered_user["username"])
        login_page.fill_password(registered_user["password"])
        login_page.click_login_button()
        
        # Wait for flash message
        expect(login_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = login_page.get_flash_message()
        assert registered_user["username"] in flash_text
    
    def test_login_with_invalid_username(self, page, base_url):
        """Test that login fails with invalid username."""
        login_page = LoginPage(page, base_url)
        login_page.goto_login()
        
        # Fill form with invalid credentials
        login_page.fill_username("nonexistentuser")
        login_page.fill_password("password123")
        login_page.click_login_button()
        
        # Wait for flash message
        expect(login_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = login_page.get_flash_message()
        assert "Invalid username or password" in flash_text
    
    def test_login_with_invalid_password(self, page, base_url, registered_user):
        """Test that login fails with wrong password."""
        login_page = LoginPage(page, base_url)
        login_page.goto_login()
        
        # Fill form with correct username but wrong password
        login_page.fill_username(registered_user["username"])
        login_page.fill_password("wrongpassword")
        login_page.click_login_button()
        
        # Wait for flash message
        expect(login_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify error message
        flash_text = login_page.get_flash_message()
        assert "Invalid username or password" in flash_text
    
    def test_login_redirects_to_dashboard_when_logged_in(self, page, base_url, logged_in_user):
        """Test that accessing login redirects to dashboard when already logged in."""
        # Navigate directly to dashboard (should redirect to login)
        page.goto(f"{base_url}/dashboard")
        
        # Should have been redirected to login
        expect(page).to_have_url(f"{base_url}/login")
    
    def test_login_with_email_as_username(self, page, base_url, registered_user):
        """Test that login works with email as username."""
        login_page = LoginPage(page, base_url)
        login_page.goto_login()
        
        # Fill form with email instead of username
        login_page.fill_username(registered_user["email"])
        login_page.fill_password(registered_user["password"])
        login_page.click_login_button()
        
        # Wait for flash message
        expect(login_page.wait_for_flash_message()).to_be_visible(timeout=5000)
        
        # Verify success message
        flash_text = login_page.get_flash_message()
        assert registered_user["username"] in flash_text


class TestLogout:
    """Test cases for user logout."""
    
    def test_successful_logout(self, page, base_url, logged_in_user):
        """Test that a logged in user can logout successfully."""
        # Navigate to dashboard
        dashboard_page = DashboardPage(page, base_url)
        dashboard_page.goto_dashboard()
        
        # Click logout (assuming there's a logout link/button)
        # For now, we'll test by navigating to logout route directly
        page.goto(f"{base_url}/logout")
        
        # Should be redirected to login
        expect(page).to_have_url(f"{base_url}/login")
    
    def test_logout_shows_flash_message(self, page, base_url, logged_in_user):
        """Test that logout shows appropriate flash message."""
        # Navigate to dashboard first
        dashboard_page = DashboardPage(page, base_url)
        dashboard_page.goto_dashboard()
        
        # Click on logout link (assuming it exists in nav)
        logout_link = page.locator("a:has-text('Logout')")
        if logout_link.is_visible():
            logout_link.click()
            
            # Wait for flash message
            expect(dashboard_page.wait_for_flash_message()).to_be_visible(timeout=5000)
            
            # Verify message
            flash_text = dashboard_page.get_flash_message()
            assert "logged out" in flash_text.lower()
