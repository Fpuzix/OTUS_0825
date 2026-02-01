import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)
        return self

    def wait_visible(self, locator, timeout=10, name="element"):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Timeout: {name} not visible after {timeout}s. locator={locator}",
        )

    def wait_clickable(self, locator, timeout=10, name="element"):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Timeout: {name} not clickable after {timeout}s. locator={locator}",
        )

    def optional_visible(self, locator, timeout=3, poll=0.2):
        end = time.time() + timeout
        while time.time() < end:
            els = self.driver.find_elements(*locator)
            if els and els[0].is_displayed():
                return els[0]
            time.sleep(poll)
        return None

    def click(self, locator, timeout=10, name="element"):
        self.wait_clickable(locator, timeout=timeout, name=name).click()

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def type(self, locator, text: str, timeout=10, name="input", clear=True):
        el = self.wait_visible(locator, timeout=timeout, name=name)
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    def wait_text_change(self, locator, old_text: str, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator).text != old_text
        )

    def accept_alert(self, timeout=5):
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
