from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from utils.config import USERS


class TestCheckout:
    """E2E checkout: login → add to cart → checkout → confirm."""

    def _login_and_add_to_cart(self, driver):
        LoginPage(driver).open().login(
            USERS["standard"]["username"],
            USERS["standard"]["password"]
        )
        inventory = InventoryPage(driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()
        return CheckoutPage(driver)

    def test_full_checkout_flow(self, driver):
        """Complete purchase from login to order confirmation."""
        checkout = self._login_and_add_to_cart(driver)
        checkout.proceed_to_checkout()
        checkout.fill_info("Dalu", "Pack", "11001")
        checkout.finish()
        confirmation = checkout.get_confirmation()
        assert "Thank you" in confirmation, \
            f"Unexpected confirmation: {confirmation}"

    def test_checkout_requires_first_name(self, driver):
        """Checkout form validates required first name field."""
        checkout = self._login_and_add_to_cart(driver)
        checkout.proceed_to_checkout()
        checkout.fill_info("", "Pack", "11001")
        # Should stay on step one with error OR show error message
        assert "checkout-step-one" in driver.current_url or \
               "checkout-step-two" not in driver.current_url, \
               "Should not have proceeded past step one with empty first name"
        # Check for error message
        error = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            )
        )
        assert "First Name is required" in error.text