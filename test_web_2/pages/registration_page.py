import time
import pytest

from selenium.webdriver.common.by import By

from .base_page import BasePage


class RegistrationPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='Your Store']")
    ICON_HOME = (By.CSS_SELECTOR, ".fas.fa-home")
    SEARCH = (By.CSS_SELECTOR, 'input[placeholder="Search"]')
    CART_BTN = (By.CSS_SELECTOR, "button[data-bs-toggle='dropdown'].btn-block")
    ICON_USER = (By.CSS_SELECTOR, ".fa-user")

    FIRSTNAME = (By.ID, "input-firstname")
    LASTNAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    H1 = (By.CSS_SELECTOR, "h1")

    SUCCESS_H1_CREATED = (By.XPATH, "//h1[contains(text(), 'Created')]")

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

    def register_simple_and_assert_created(
        self, firstname="Ivan", lastname="Ivanov", password="password123"
    ):
        self.type(self.FIRSTNAME, firstname, name="Имя")
        self.type(self.LASTNAME, lastname, name="Фамилия")

        email = f"test{int(time.time())}@mail.ru"
        self.type(self.EMAIL, email, name="Email")

        tel = self.driver.find_elements(*self.TELEPHONE)
        if tel:
            tel[0].send_keys("1234567890")

        self.type(self.PASSWORD, password, name="Пароль")

        agree = self.wait_visible(self.AGREE, name="Чекбокс соглашения")
        self.js_click(agree)

        submit_button = self.wait_visible(self.SUBMIT, name="Кнопка")
        self.scroll_into_view(submit_button)
        submit_button.click()

        success = self.wait_visible(
            self.SUCCESS_H1_CREATED, name="Заголовок успеха", timeout=10
        )
        assert "Created" in success.text

    def register_new_user_and_assert_success(self):
        self.type(self.FIRSTNAME, "Ivan", name="Firstname")
        self.type(self.LASTNAME, "Testerov", name="Lastname")

        email = f"test_user_{int(time.time())}@example.com"
        self.driver.find_element(*self.EMAIL).send_keys(email)

        telephones = self.driver.find_elements(*self.TELEPHONE)
        if telephones:
            telephones[0].send_keys("1234567890")

        self.driver.find_element(*self.PASSWORD).send_keys("test_password_2026")

        agree_check = self.driver.find_element(*self.AGREE)
        self.scroll_into_view(agree_check)
        self.js_click(agree_check)

        submit_button = self.driver.find_element(*self.SUBMIT)
        self.js_click(submit_button)

        time.sleep(2)

        current_h1 = self.wait_visible(self.H1, name="h1").text

        if current_h1 == "Register Account":
            errors = self.driver.find_elements(
                By.CSS_SELECTOR, ".text-danger, .alert-danger, .invalid-feedback"
            )
            error_list = [e.text for e in errors if e.text]
            if not error_list:
                pytest.fail(
                    "Форма не была отправлена (ошибок нет, но мы всё еще на странице регистрации)."
                )
            pytest.fail(f"Регистрация не удалась. Ошибки: {error_list}")

        assert current_h1 == "Your Account Has Been Created!"
