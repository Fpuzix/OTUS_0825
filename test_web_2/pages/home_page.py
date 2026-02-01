from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    BANNER_IPHONE = (By.CSS_SELECTOR, 'img[alt="iPhone 6"]')
    CART_BUTTON_TEXT = (By.XPATH, '//button[contains(., "item(s)")]')
    MACBOOK_IMG = (By.CSS_SELECTOR, 'img[alt="MacBook"]')
    CONTACT_US = (By.XPATH, '//a[text()="Contact Us"]')

    PRICE_NEW = (By.CSS_SELECTOR, ".price-new")
    DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a.dropdown-toggle")
    EURO_LINK = (By.XPATH, "//a[contains(., 'Euro')]")

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
        price_el = self.wait_visible(self.PRICE_NEW, name="Старая цена")
        initial_text = price_el.text

        self.driver.find_element(*self.DROPDOWN_TOGGLE).click()

        euro_link = self.wait_visible(self.EURO_LINK, name="Ссылка Euro")
        self.js_click(euro_link)

        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.PRICE_NEW).text != initial_text
        )

        new_price_text = self.driver.find_element(*self.PRICE_NEW).text
        assert "€" in new_price_text, (
            f"Ожидался символ €, но получили: {new_price_text}"
        )
