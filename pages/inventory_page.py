from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE       = (By.CLASS_NAME, "title")
    ADD_TO_CART = (By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']")
    REMOVE_BTN  = (By.CSS_SELECTOR, "[data-test='remove-sauce-labs-backpack']")
    CART_BADGE  = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK   = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BTN    = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_on_inventory(self):
        return "inventory" in self.get_url()

    def get_title(self):
        return self.get_text(self.TITLE)

    def add_backpack_to_cart(self):
        # Click add to cart
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART)).click()
        # Wait for the button to change to "Remove" — confirms item was added
        self.wait.until(EC.presence_of_element_located(self.REMOVE_BTN))
        time.sleep(0.5)
        return self

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        cart = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        self.driver.execute_script("arguments[0].click();", cart)
        self.wait.until(lambda d: "cart" in d.current_url)

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU_BTN)).click()
        time.sleep(1)
        logout = self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        self.driver.execute_script("arguments[0].click();", logout)
        self.wait.until(lambda d: "inventory" not in d.current_url)