from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    CHECKOUT_BTN   = (By.ID, "checkout")
    FIRST_NAME     = (By.ID, "first-name")
    LAST_NAME      = (By.ID, "last-name")
    ZIP_CODE       = (By.ID, "postal-code")
    CONTINUE_BTN   = (By.ID, "continue")
    FINISH_BTN     = (By.ID, "finish")
    CONFIRM_HEADER = (By.CLASS_NAME, "complete-header")
    ERROR          = (By.CSS_SELECTOR, "[data-test='error']")

    def proceed_to_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(lambda d: "checkout-step-one" in d.current_url)
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME))
        time.sleep(0.8)
        return self

    def _react_fill(self, element_id, value):
        """Fill a React controlled input by directly setting its internal state."""
        self.driver.execute_script("""
            var el = document.getElementById(arguments[0]);
            var nativeInput = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            );
            nativeInput.set.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
        """, element_id, value)
        time.sleep(0.2)

    def fill_info(self, first, last, zip_code):
        print(f"\n>>> fill_info: first='{first}' last='{last}' zip='{zip_code}'")

        self._react_fill("first-name", first)
        self._react_fill("last-name", last)
        self._react_fill("postal-code", zip_code)

        # Verify values via JS
        fn = self.driver.execute_script("return document.getElementById('first-name').value;")
        ln = self.driver.execute_script("return document.getElementById('last-name').value;")
        zp = self.driver.execute_script("return document.getElementById('postal-code').value;")
        print(f">>> Fields — first:'{fn}' last:'{ln}' zip:'{zp}'")

        time.sleep(0.3)
        cont = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN))
        self.driver.execute_script("arguments[0].click();", cont)
        time.sleep(1)
        print(f">>> URL after continue: {self.driver.current_url}")
        return self

    def finish(self):
        print(f"\n>>> finish() — URL: {self.driver.current_url}")
        self.wait.until(lambda d: "checkout-step-two" in d.current_url)
        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        return self

    def get_confirmation(self):
        return self.get_text(self.CONFIRM_HEADER)

    def get_error(self):
        return self.wait.until(
            EC.presence_of_element_located(self.ERROR)
        ).text