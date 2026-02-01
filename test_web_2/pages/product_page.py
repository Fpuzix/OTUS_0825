from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class ProductPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    ICON_HOME = (By.CSS_SELECTOR, ".fas.fa-home")
    SEARCH = (By.CSS_SELECTOR, 'input[placeholder="Search"]')
    BUTTON_CART = (By.ID, "button-cart")
    FOOTER_OPENCART = (By.LINK_TEXT, "OpenCart")

    EX_TAX = (By.XPATH, "//li[contains(text(), 'Ex Tax: ')]")
    PRICE_NEW = (By.CSS_SELECTOR, ".price-new")
    DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a.dropdown-toggle")
    EURO_LINK = (By.XPATH, "//a[contains(., 'Euro')]")

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
        price_element = self.wait_visible(self.EX_TAX, name="Цена Ex Tax")
        clean_price = "".join(c for c in price_element.text if c.isdigit() or c == ".")
        price_value = float(
            clean_price
        )  # если не распарсится — упадёт, и это нормально
        assert price_value > 0, f"Цена товара некорректна: {price_value}"

    def switch_currency_to_euro_and_assert(self):
        price_el = self.wait_visible(self.PRICE_NEW, name="Старая цена")
        initial_text = price_el.text

        self.driver.find_element(*self.DROPDOWN_TOGGLE).click()

        euro_link = self.wait_visible(self.EURO_LINK, name="Ссылка Euro")
        self.js_click(euro_link)

        WebDriverWait(self.driver, 10).until_not(
            EC.text_to_be_present_in_element(self.PRICE_NEW, initial_text)
        )

        new_price_text = self.driver.find_element(*self.PRICE_NEW).text
        assert "€" in new_price_text, (
            f"Ожидался символ €, но получили: {new_price_text}"
        )
