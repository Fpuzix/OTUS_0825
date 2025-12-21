import pytest
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


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

    driver.get(url)

    request.addfinalizer(driver.quit)

    return driver


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")
