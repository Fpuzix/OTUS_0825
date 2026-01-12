import pytest
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))
    parser.addoption("--url", default="http://192.168.0.171:8081/")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    drivers = request.config.getoption("--drivers")
    url = request.config.getoption("--url")

    if browser_name == "chrome":
        service = Service()
        driver = webdriver.Chrome(service=service)
    elif browser_name == "yandex":
        options = webdriver.ChromeOptions()
        service = Service(executable_path=os.path.join(drivers, "yandexdriver.exe"))
        options.binary_location = (
            "C:/Users/F/AppData/Local/Yandex/YandexBrowser/Application/browser.exe"
        )
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("Driver not supported")

    driver.implicitly_wait(5)
    driver.maximize_window()

    if url:
        driver.get(url)

    yield driver
    driver.quit()
    return driver


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture
def url_catalog(base_url):
    return f"{base_url}/en-gb/catalog/smartphone"


@pytest.fixture
def url_goods(base_url):
    return f"{base_url}/en-gb/product/desktops/canon-eos-5d"


@pytest.fixture
def url_administration(base_url):
    return f"{base_url}/administration/"


@pytest.fixture
def url_registration(base_url):
    return f"{base_url}/index.php?route=account/register"


@pytest.fixture
def get_wait(browser):
    def _wait(timeout=10):
        return WebDriverWait(browser, timeout)

    return _wait


@pytest.fixture
def wait_element(browser):
    def _wait(locator, timeout=10, poll=0.2, name="element"):
        try:
            return WebDriverWait(browser, timeout, poll_frequency=poll).until(
                EC.visibility_of_element_located(locator),
                message=f"Timeout: {name} not visible after {timeout}s. locator={locator}",
            )
        except TimeoutException:
            return None

    return _wait
