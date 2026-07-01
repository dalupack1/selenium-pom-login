import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import USERS


class TestLogin:
    """Login test suite against SauceDemo (https://www.saucedemo.com)."""

    def test_valid_login(self, driver):
        """Standard user can log in and land on inventory page."""
        login = LoginPage(driver).open()
        login.login(USERS["standard"]["username"], USERS["standard"]["password"])
        inventory = InventoryPage(driver)
        assert inventory.is_on_inventory(), "Expected to be on inventory page after login"
        assert inventory.get_title() == "Products"

    def test_invalid_password(self, driver):
        """Wrong password shows error message."""
        login = LoginPage(driver).open()
        login.login(USERS["standard"]["username"], "wrong_password")
        assert login.is_error_displayed(), "Error message should appear"
        assert "Username and password do not match" in login.get_error()

    def test_locked_out_user(self, driver):
        """Locked-out user sees locked error."""
        login = LoginPage(driver).open()
        login.login(USERS["locked"]["username"], USERS["locked"]["password"])
        assert login.is_error_displayed()
        assert "locked out" in login.get_error().lower()

    def test_empty_username(self, driver):
        """Submitting with empty username shows validation error."""
        login = LoginPage(driver).open()
        login.login("", "secret_sauce")
        assert login.is_error_displayed()
        assert "Username is required" in login.get_error()

    def test_empty_password(self, driver):
        """Submitting with empty password shows validation error."""
        login = LoginPage(driver).open()
        login.login("standard_user", "")
        assert login.is_error_displayed()
        assert "Password is required" in login.get_error()

    def test_logout_flow(self, driver):
        """User can log in and successfully log out."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        login = LoginPage(driver).open()
        login.login(USERS["standard"]["username"], USERS["standard"]["password"])
        inventory = InventoryPage(driver)
        inventory.logout()
        # Wait until we're no longer on the inventory page
        WebDriverWait(driver, 10).until(
            lambda d: "inventory" not in d.current_url
        )
        assert "inventory" not in driver.current_url