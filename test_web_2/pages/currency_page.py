import time

from selenium.webdriver.common.by import By

from .base_page import BasePage


class CurrencyPage(BasePage):
    DROPDOWN = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    CART_VALUE = (By.CSS_SELECTOR, "#header-cart button")
    ANY_PRICE = (By.CSS_SELECTOR, ".price-new, .price")

    def switch_currency(self, currency_name: str):
        dropdown = self.wait_visible(self.DROPDOWN, name="Currency dropdown")
        self.scroll_into_view(dropdown)
        dropdown.click()

        time.sleep(0.5)

        currency_option_xpath = (
            f"//ul[@class='dropdown-menu show']//button[contains(text(), '{currency_name}')]"
            f" | //ul[@class='dropdown-menu show']//a[contains(text(), '{currency_name}')]"
            f" | //button[contains(@name, '{currency_name[:3].upper()}')]"
        )

        btn = self.wait_clickable(
            (By.XPATH, currency_option_xpath),
            timeout=5,
            name=f"Currency {currency_name}",
        )
        btn.click()

        time.sleep(1.5)

    def assert_symbol_applied(self, symbol: str, currency_name: str):
        cart_val = self.wait_visible(self.CART_VALUE, name="Cart").text
        product_price = self.driver.find_element(*self.ANY_PRICE).text
        assert (symbol in cart_val) or (symbol in product_price), (
            f"Валюта {currency_name} не применилась! "
            f"Ожидали {symbol}. В корзине: {cart_val}, в товаре: {product_price}"
        )
