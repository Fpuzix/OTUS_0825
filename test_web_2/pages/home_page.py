from selenium.webdriver.common.by import By

from .base_page import BasePage


class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    BANNER_IPHONE = (By.CSS_SELECTOR, 'img[alt="iPhone 6"]')
    CART_BUTTON_TEXT = (By.XPATH, '//button[contains(., "item(s)")]')
    MACBOOK_IMG = (By.CSS_SELECTOR, 'img[alt="MacBook"]')
    CONTACT_US = (By.XPATH, '//a[text()="Contact Us"]')

    PRICE_ANY = (By.CSS_SELECTOR, ".price-new, .price")
    DROPDOWN_TOGGLE = (
        By.CSS_SELECTOR,
        "#form-currency .dropdown-toggle, a.dropdown-toggle",
    )
    EURO_LINK = (By.XPATH, "//a[contains(., 'Euro')] | //button[contains(., 'Euro')]")

    @property
    def page_marker(self):
        return self.LOGO

    def logo_displayed(self) -> bool:
        return self.driver.find_element(*self.LOGO).is_displayed()

    def banner_displayed(self) -> bool:
        return self.driver.find_element(*self.BANNER_IPHONE).is_displayed()

    def cart_button_displayed(self) -> bool:
        return self.driver.find_element(*self.CART_BUTTON_TEXT).is_displayed()

    def macbook_img_displayed(self) -> bool:
        return self.driver.find_element(*self.MACBOOK_IMG).is_displayed()

    def contact_us_displayed(self) -> bool:
        return self.driver.find_element(*self.CONTACT_US).is_displayed()

    def switch_currency_to_euro_and_assert(self):
        initial_text = self.text(self.PRICE_ANY, name="Цена")

        self.click(self.DROPDOWN_TOGGLE, name="Currency dropdown")
        self.click(self.EURO_LINK, name="Euro")

        self.wait_text_change(self.PRICE_ANY, initial_text, timeout=10, name="Цена")

        new_price_text = self.driver.find_element(*self.PRICE_ANY).text
        assert "€" in new_price_text, (
            f"Ожидался символ €, но получили: {new_price_text}"
        )
