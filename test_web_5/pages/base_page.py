import logging
import time
from abc import ABC, abstractmethod


import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


class BasePage(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.log = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def page_marker(self):
        raise NotImplementedError

    def _wait(self, timeout: int = 10):
        return WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
                ElementClickInterceptedException,
            ),
        )

    @allure.step("Open: {url}")
    def open(self, url: str, timeout: int = 10):
        self.log.info("open url=%s", url)
        self.driver.get(url)
        self.wait_visible(self.page_marker, timeout=timeout, name="page marker")
        return self

    def wait_visible(self, locator, timeout: int = 10, name: str = "element"):
        return self._wait(timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Timeout: {name} not visible after {timeout}s. locator={locator}",
        )

    def wait_clickable(self, locator, timeout: int = 10, name: str = "element"):
        return self._wait(timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Timeout: {name} not clickable after {timeout}s. locator={locator}",
        )

    def wait_text_change(
        self, locator, old_text: str, timeout: int = 10, name: str = "text"
    ):
        self._wait(timeout).until(
            lambda d: d.find_element(*locator).text != old_text,
            message=f"Timeout: {name} not changed after {timeout}s. locator={locator}",
        )

    @allure.step("Click: {name}")
    def click(self, locator, timeout: int = 10, name: str = "element"):
        self.log.info("click name=%s locator=%s", name, locator)

        def _do(d):
            el = d.find_element(*locator)
            el.click()
            return True

        self._wait(timeout).until(
            _do, message=f"Timeout: can't click {name}. locator={locator}"
        )

    @allure.step("Type: {name}")
    def type(
        self,
        locator,
        text: str,
        timeout: int = 10,
        name: str = "input",
        clear: bool = True,
    ):
        self.log.info("type name=%s locator=%s", name, locator)
        el = self.wait_visible(locator, timeout=timeout, name=name)
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    def text(self, locator, timeout: int = 10, name: str = "element") -> str:
        return self.wait_visible(locator, timeout=timeout, name=name).text

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def optional_visible(self, locator, timeout: float = 3.0, poll: float = 0.2):
        end = time.time() + timeout
        while time.time() < end:
            els = self.driver.find_elements(*locator)
            if els and els[0].is_displayed():
                return els[0]
            time.sleep(poll)
        return None

    @allure.step("Accept alert")
    def accept_alert(self, timeout: int = 5):
        self.log.info("accept_alert timeout=%s", timeout)
        self._wait(timeout).until(
            EC.alert_is_present(),
            message=f"Timeout: alert not present after {timeout}s",
        )
        self.driver.switch_to.alert.accept()
