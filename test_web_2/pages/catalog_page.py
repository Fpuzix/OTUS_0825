import random

from selenium.webdriver.common.by import By

from .base_page import BasePage


class CatalogPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    ICON_HOME = (By.CSS_SELECTOR, ".fas.fa-home")
    ICON_CART = (By.CSS_SELECTOR, ".fa-solid.fa-cart-shopping")
    PAGES_INFO = (By.CSS_SELECTOR, "div.col-sm-6.text-end")
    FOOTER_OPENCART = (By.LINK_TEXT, "OpenCart")

    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "button[formaction*='checkout/cart.add']")
    PRODUCT_THUMB_ANCESTOR = (By.XPATH, "./ancestor::div[@class='product-thumb']")
    PRODUCT_NAME_IN_CARD = (By.CSS_SELECTOR, "h4 a")

    ALERT_CLOSE = (By.CSS_SELECTOR, ".alert-success .btn-close")
    CART_BUTTON = (By.CSS_SELECTOR, "button.btn-inverse")

    def logo_displayed(self) -> bool:
        return self.driver.find_element(*self.LOGO).is_displayed()

    def home_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_HOME).is_displayed()

    def cart_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_CART).is_displayed()

    def pages_info_displayed(self) -> bool:
        return self.driver.find_element(*self.PAGES_INFO).is_displayed()

    def footer_link_displayed(self) -> bool:
        return self.driver.find_element(*self.FOOTER_OPENCART).is_displayed()

    def home_icon_present(self):
        icon = self.wait_visible(self.ICON_HOME, name="Иконка дома")
        assert icon is not None and icon.is_displayed(), (
            "Иконка 'Домой' не найдена/не отображается"
        )

    def add_random_product_to_cart_and_assert_in_dropdown(self):
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        assert len(btns) > 0, "На странице нет товаров для добавления"

        target_button = btns[random.randint(0, len(btns) - 1)]

        product_card = target_button.find_element(*self.PRODUCT_THUMB_ANCESTOR)
        product_name = product_card.find_element(*self.PRODUCT_NAME_IN_CARD).text

        self.scroll_into_view(target_button)
        target_button.click()

        if "route=product/product" in self.driver.current_url:
            btn_on_page = self.wait_visible(
                (By.ID, "button-cart"), name="Кнопка в карточке"
            )
            btn_on_page.click()

        close_btn = self.optional_visible(self.ALERT_CLOSE, timeout=3)
        if close_btn:
            close_btn.click()

        self.wait_visible(self.CART_BUTTON, name="Кнопка корзины")
        cart_button = self.driver.find_element(*self.CART_BUTTON)
        self.js_click(cart_button)

        product_in_cart = self.wait_visible(
            (
                By.XPATH,
                f"//div[@id='header-cart']//a[contains(text(), '{product_name}')]",
            ),
            name=f"Товар {product_name} в корзине",
            timeout=10,
        )

        assert product_in_cart is not None, (
            f"Товар '{product_name}' не найден в корзине после добавления"
        )
