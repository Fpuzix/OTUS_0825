import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from .base_page import BasePage


class RegistrationPage(BasePage):
    # Хедер/общие элементы
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    ICON_HOME = (By.CSS_SELECTOR, ".fas.fa-home")
    SEARCH = (By.CSS_SELECTOR, 'input[placeholder="Search"]')
    CART_BTN = (By.CSS_SELECTOR, "#header-cart button")
    ICON_USER = (By.CSS_SELECTOR, ".fa-user")

    # Поля формы регистрации
    FIRSTNAME = (By.ID, "input-firstname")
    LASTNAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    H1 = (By.CSS_SELECTOR, "h1")

    # Успешная регистрация
    SUCCESS_H1_CREATED = (By.XPATH, "//h1[contains(., 'Created')]")

    @property
    def page_marker(self):
        return self.FIRSTNAME

    def logo_displayed(self) -> bool:
        return self.driver.find_element(*self.LOGO).is_displayed()

    def home_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_HOME).is_displayed()

    def search_displayed(self) -> bool:
        return self.driver.find_element(*self.SEARCH).is_displayed()

    def cart_button_displayed(self) -> bool:
        return self.driver.find_element(*self.CART_BTN).is_displayed()

    def user_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_USER).is_displayed()

    def _invalid_fields(self):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll(':invalid')).map(e => ({id:e.id,name:e.name,msg:e.validationMessage}));"
        )

    def _fill_common_fields(
        self, firstname: str, lastname: str, email: str, password: str
    ):
        self.type(self.FIRSTNAME, firstname, name="Firstname")
        self.type(self.LASTNAME, lastname, name="Lastname")
        self.type(self.EMAIL, email, name="Email")

        tel = self.driver.find_elements(*self.TELEPHONE)
        if tel:
            tel[0].clear()
            tel[0].send_keys("1234567890")

        self.type(self.PASSWORD, password, name="Password")

        confirm = self.driver.find_elements(*self.CONFIRM)
        if confirm:
            confirm[0].clear()
            confirm[0].send_keys(password)

        agree = self.wait_visible(self.AGREE, name="Agree checkbox")
        self.scroll_into_view(agree)
        if not agree.is_selected():
            self.js_click(agree)

    def register_simple_and_assert_created(
        self, firstname="Ivan", lastname="Ivanov", password="password123"
    ):
        email = f"test{int(time.time())}@mail.ru"
        self._fill_common_fields(firstname, lastname, email, password)

        submit = self.wait_clickable(self.SUBMIT, name="Submit")
        self.scroll_into_view(submit)
        submit.click()

        success = self.wait_visible(
            self.SUCCESS_H1_CREATED, name="Success H1", timeout=10
        )
        assert "Created" in success.text

    def register_new_user_and_assert_success(self):
        email = f"test_user_{int(time.time())}@example.com"
        password = "test_password_2026"

        self._fill_common_fields("Ivan", "Testerov", email, password)

        old_url = self.driver.current_url
        old_h1 = self.wait_visible(self.H1, name="h1").text

        submit = self.wait_clickable(self.SUBMIT, name="Submit")
        self.scroll_into_view(submit)
        submit.click()

        WebDriverWait(self.driver, 10).until(
            lambda d: (len(d.find_elements(*self.SUCCESS_H1_CREATED)) > 0)
            or ("success" in d.current_url)
            or (d.current_url != old_url)
            or (d.find_element(*self.H1).text != old_h1)
            or (
                len(
                    d.find_elements(
                        By.CSS_SELECTOR,
                        ".text-danger, .alert-danger, .invalid-feedback",
                    )
                )
                > 0
            )
            or (len(self._invalid_fields()) > 0)
        )

        if self.driver.find_elements(*self.SUCCESS_H1_CREATED):
            return self

        current_h1 = self.wait_visible(self.H1, name="h1").text

        errors = self.driver.find_elements(
            By.CSS_SELECTOR, ".text-danger, .alert-danger, .invalid-feedback"
        )
        error_list = [e.text for e in errors if e.text]

        invalid = self._invalid_fields()
        if invalid:
            pytest.fail(f"Форма не отправилась из-за HTML5-валидации: {invalid}")

        if current_h1 == "Register Account" and not error_list:
            pytest.fail(
                "Форма не была отправлена (ошибок в DOM нет, но мы всё еще на странице регистрации)."
            )

        if error_list:
            pytest.fail(f"Регистрация не удалась. Ошибки: {error_list}")

        pytest.fail(f"Регистрация не удалась. Заголовок страницы: {current_h1}")
