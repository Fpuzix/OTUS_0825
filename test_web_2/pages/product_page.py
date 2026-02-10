import re

from selenium.webdriver.common.by import By

from .base_page import BasePage


class ProductPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    ICON_HOME = (By.CSS_SELECTOR, ".fas.fa-home")
    SEARCH = (By.CSS_SELECTOR, 'input[placeholder="Search"]')
    BUTTON_CART = (By.ID, "button-cart")
    FOOTER_OPENCART = (By.LINK_TEXT, "OpenCart")

    EX_TAX = (By.XPATH, "//li[contains(., 'Ex Tax:')]")
    PRICE_ANY = (By.CSS_SELECTOR, ".price-new, .price")

    DROPDOWN_TOGGLE = (
        By.CSS_SELECTOR,
        "#form-currency .dropdown-toggle, a.dropdown-toggle",
    )
    EURO_LINK = (By.XPATH, "//a[contains(., 'Euro')] | //button[contains(., 'Euro')]")

    @property
    def page_marker(self):
        return self.BUTTON_CART

    def logo_displayed(self) -> bool:
        return self.driver.find_element(*self.LOGO).is_displayed()

    def home_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_HOME).is_displayed()

    def search_displayed(self) -> bool:
        return self.driver.find_element(*self.SEARCH).is_displayed()

    def cart_button_displayed(self) -> bool:
        return self.driver.find_element(*self.BUTTON_CART).is_displayed()

    def footer_link_displayed(self) -> bool:
        return self.driver.find_element(*self.FOOTER_OPENCART).is_displayed()

    def assert_ex_tax_price_positive(self):
        text = self.text(self.EX_TAX, name="Цена Ex Tax")

        m = re.search(r"(\d+(?:[\.,]\d+)?)", text)
        assert m, f"Не удалось извлечь число из Ex Tax: '{text}'"

        price_value = float(m.group(1).replace(",", "."))
        assert price_value > 0, f"Цена товара некорректна: {price_value}"

    def switch_currency_to_euro_and_assert(self):
        initial_text = self.text(self.PRICE_ANY, name="Цена")

        self.click(self.DROPDOWN_TOGGLE, name="Currency dropdown")
        self.click(self.EURO_LINK, name="Euro")

        self.wait_text_change(self.PRICE_ANY, initial_text, timeout=10, name="Цена")

        new_price_text = self.driver.find_element(*self.PRICE_ANY).text
        assert "€" in new_price_text, (
            f"Ожидался символ €, но получили: {new_price_text}"
        )
