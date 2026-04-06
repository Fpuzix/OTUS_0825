import pytest
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from report_client import ReportClient


def pytest_sessionstart(session):
    try:
        ReportClient.delete_report_data()
    except Exception as e:
        print(f"Ошибка очистки: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("driver")
        if driver:
            status = "PASSED" if rep.passed else "FAILED"
            error = None if rep.passed else str(rep.longrepr)

            ReportClient.set_test_info(driver, item.name, status, error)
            print(f"[REPORT] {item.name} -> {status}")


@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()


def pytest_sessionfinish(session, exitstatus):
    print("\n[Reporting] Генерация HTML-отчета...")
    html_content = ReportClient.get_report()

    if html_content:
        report_path = os.path.join(os.getcwd(), "report.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[SUCCESS] Отчет сохранен: {report_path}")
    else:
        print("[ERROR] Не удалось получить отчет от сервера.")
