from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


from .base_page import BasePage


class CurrencyPage(BasePage):
    DROPDOWN = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    CART_VALUE = (By.CSS_SELECTOR, "#header-cart button")
    ANY_PRICE = (By.CSS_SELECTOR, ".price-new, .price")
    MENU_SHOW = (By.CSS_SELECTOR, "ul.dropdown-menu.show")

    @property
    def page_marker(self):
        return self.DROPDOWN

    def switch_currency(self, currency_name: str):
        old_cart = self.text(self.CART_VALUE, name="Cart")
        prices = self.driver.find_elements(*self.ANY_PRICE)
        old_price = prices[0].text if prices else ""

        self.click(self.DROPDOWN, name="Currency dropdown")
        self.wait_visible(self.MENU_SHOW, timeout=5, name="Currency menu")

        currency_option_xpath = (
            f"//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]"
            f"//button[contains(., '{currency_name}')]"
            f" | "
            f"//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]"
            f"//a[contains(., '{currency_name}')]"
            f" | "
            f"//button[contains(@name, '{currency_name[:3].upper()}')]"
        )

        self.click(
            (By.XPATH, currency_option_xpath),
            timeout=10,
            name=f"Currency {currency_name}",
        )

        WebDriverWait(
            self.driver, 10, ignored_exceptions=(StaleElementReferenceException,)
        ).until(
            lambda d: d.find_element(*self.CART_VALUE).text != old_cart
            or (
                d.find_elements(*self.ANY_PRICE)
                and d.find_elements(*self.ANY_PRICE)[0].text != old_price
            )
        )

    def assert_symbol_applied(self, symbol: str, currency_name: str):
        cart_val = self.text(self.CART_VALUE, name="Cart")
        product_price = self.driver.find_element(*self.ANY_PRICE).text
        assert (symbol in cart_val) or (symbol in product_price), (
            f"Валюта {currency_name} не применилась! "
            f"Ожидали {symbol}. В корзине: {cart_val}, в товаре: {product_price}"
        )
