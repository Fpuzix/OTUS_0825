from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminLoginPage(BasePage):
    # UI элементы страницы логина
    LOGO = (By.CSS_SELECTOR, "img[title='OpenCart']")
    ICON_LOCK = (By.CSS_SELECTOR, ".fa-lock")
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Username"]')
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].btn-primary")
    ICON_USER = (By.CSS_SELECTOR, ".fa-user")

    # Поля формы логина
    INPUT_USERNAME = (By.ID, "input-username")
    INPUT_PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    # После логина
    NAV_PROFILE = (By.ID, "nav-profile")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'route=common/logout')]")

    @property
    def page_marker(self):
        return self.INPUT_USERNAME

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
        self.type(self.INPUT_USERNAME, username, name="Поле логина")
        self.type(self.INPUT_PASSWORD, password, name="Поле пароля")
        self.click(self.LOGIN_BTN, name="Кнопка Login")

        self.wait_visible(self.NAV_PROFILE, name="Профиль админа")
        return self

    def logout_and_assert_back_to_login(self):
        self.click(self.NAV_PROFILE, name="Меню профиля")
        self.click(self.LOGOUT_LINK, name="Logout")

        username_after = self.wait_visible(
            self.INPUT_USERNAME, name="Поле логина после выхода"
        )
        assert username_after.is_displayed(), "После выхода поле логина не отображается"
        return self
