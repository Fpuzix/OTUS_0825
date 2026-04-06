import time
from appium.webdriver.common.appiumby import AppiumBy


def test_scroll_to_calendar(driver):
    # 1) Нажимаем на кнопку Home
    driver.press_keycode(3)
    time.sleep(2)

    # 2) Открываем меню
    size = driver.get_window_size()
    driver.swipe(
        size["width"] / 2,
        size["height"] * 0.8,
        size["width"] / 2,
        size["height"] * 0.2,
        600,
    )
    time.sleep(2)

    # 3) Ищем календарь
    ui_selector = (
        "new UiScrollable(new UiSelector().scrollable(true).instance(0))"
        '.scrollIntoView(new UiSelector().textMatches("(?i)Calendar|Календарь").instance(0))'
    )

    calendar_app = driver.find_element(
        by=AppiumBy.ANDROID_UIAUTOMATOR, value=ui_selector
    )
    calendar_app.click()
    time.sleep(2)
