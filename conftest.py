import os
import logging
from pathlib import Path

import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--browser_version", default=None)
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")
    parser.addoption(
        "--executor", default="auto", choices=["auto", "local", "selenoid", "ggr"]
    )
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))
    parser.addoption("--url", default="http://opencart:8080/")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")
    drivers = request.config.getoption("--drivers")
    url = request.config.getoption("--url")

    headless = request.config.getoption("--headless")

    remote_url = os.getenv("SELENOID_URL") or os.getenv("SELENIUM_REMOTE_URL")

    if executor == "local":
        use_remote = False
    elif executor in ("selenoid", "ggr"):
        use_remote = True
        if not remote_url:
            raise RuntimeError(
                "executor задан как remote (selenoid/ggr), но не задан SELENOID_URL/SELENIUM_REMOTE_URL"
            )
    else:
        use_remote = bool(remote_url)

    if use_remote:
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        else:
            raise Exception("Remote driver supports only chrome/firefox")


        if headless:
            options.add_argument("--headless")

        options.set_capability("browserName", browser_name)
        if browser_version:
            options.set_capability("browserVersion", browser_version)

        options.set_capability(
            "selenoid:options",
            {
                "enableVNC": True,
                "screenResolution": "1920x1080x24",
            },
        )

        driver = webdriver.Remote(command_executor=remote_url, options=options)
        driver.set_window_size(1920, 1080)

    else:

        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")

                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

            service = Service()
            driver = webdriver.Chrome(service=service, options=options)

        elif browser_name == "yandex":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")


            path = os.path.join(drivers, "yandexdriver") if drivers else "yandexdriver"
            service = Service(executable_path=path)

            options.binary_location = "/usr/bin/yandex-browser"
            driver = webdriver.Chrome(service=service, options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)

        else:
            raise Exception("Driver not supported")


        if not headless:
            driver.maximize_window()
        else:
            driver.set_window_size(1920, 1080)

    driver.implicitly_wait(5)

    if url:
        driver.get(url)

    yield driver
    driver.quit()


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture
def url_catalog(base_url):
    return f"{base_url}/en-gb/catalog/smartphone"


@pytest.fixture
def url_goods(base_url):
    return f"{base_url}/en-gb/product/cameras/nikon-d300"


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


def wait_element(browser, locator, timeout=10, poll=0.2, name="element"):
    return WebDriverWait(browser, timeout, poll_frequency=poll).until(
        EC.visibility_of_element_located(locator),
        message=f"Timeout: {name} not visible after {timeout}s. locator={locator}",
    )


def pytest_configure(config):
    log_file = Path(__file__).with_name("test_run.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.failed and rep.when in ("setup", "call"):
        driver = item.funcargs.get("browser") or item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                driver.current_url,
                name="current_url",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                driver.page_source,
                name="page_source",
                attachment_type=allure.attachment_type.HTML,
            )

        log_file = Path(__file__).with_name("test_run.log")
        if log_file.exists():
            allure.attach(
                log_file.read_text(encoding="utf-8", errors="ignore"),
                name="test_run.log",
                attachment_type=allure.attachment_type.TEXT,
            )
