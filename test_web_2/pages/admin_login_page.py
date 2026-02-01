from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminLoginPage(BasePage):
    LOGO = (By.CSS_SELECTOR, "img[title='OpenCart']")
    ICON_LOCK = (By.CSS_SELECTOR, ".fa-lock")
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Username"]')
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].btn-primary")
    ICON_USER = (By.CSS_SELECTOR, ".fa-user")

    INPUT_USERNAME = (By.ID, "input-username")
    INPUT_PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    NAV_PROFILE = (By.ID, "nav-profile")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'route=common/logout')]")

    def logo_displayed(self) -> bool:
        return self.driver.find_element(*self.LOGO).is_displayed()

    def lock_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_LOCK).is_displayed()

    def username_field_displayed(self) -> bool:
        return self.driver.find_element(*self.USERNAME_INPUT).is_displayed()

    def submit_button_displayed(self) -> bool:
        return self.driver.find_element(*self.SUBMIT_BTN).is_displayed()

    def user_icon_displayed(self) -> bool:
        return self.driver.find_element(*self.ICON_USER).is_displayed()

    def login(self, username: str, password: str):
        user_field = self.wait_visible(self.INPUT_USERNAME, name="Поле логина")
        user_field.clear()
        user_field.send_keys(username)

        pass_field = self.driver.find_element(*self.INPUT_PASSWORD)
        pass_field.clear()
        pass_field.send_keys(password)

        self.driver.find_element(*self.LOGIN_BTN).click()
        self.wait_visible(self.NAV_PROFILE, name="Профиль админа")

    def logout_and_assert_back_to_login(self):
        logout_link = self.wait_visible(self.LOGOUT_LINK, name="Кнопка выхода")
        self.js_click(logout_link)

        username_after = self.wait_visible(
            self.INPUT_USERNAME, name="Поле логина после выхода"
        )
        assert username_after.is_displayed(), "После выхода поле логина не отображается"
