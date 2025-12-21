import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_home_page_logo(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(base_url)

    logo_element = browser.find_element(By.CSS_SELECTOR, "img[title='Your Store']")

    assert logo_element.is_displayed()

    browser.implicitly_wait(0)


def test_banner_displayed(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(base_url)

    banner_element = browser.find_element(By.CSS_SELECTOR, 'img[alt="iPhone 6"]')

    assert banner_element.is_displayed(), "Баннер iPhone 6 не отображается."

    browser.implicitly_wait(0)


def test_cart_button(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(base_url)

    cart_element = browser.find_element(
        By.XPATH, '//button[contains(text(), "0 item(s) - $0.00")]'
    )

    assert cart_element.is_displayed(), "Кнопка корзины покупок не отображается."
    browser.implicitly_wait(0)


def test_good_button(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(base_url)

    good_element = browser.find_element(By.CSS_SELECTOR, 'img[alt="MacBook"]')

    assert good_element.is_displayed(), (
        "Изображение товара 'MacBook' не отображается на странице."
    )
    browser.implicitly_wait(0)


def test_contact_us(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(base_url)

    contact_element = browser.find_element(By.XPATH, '//a[text()="Contact Us"]')

    assert contact_element.is_displayed(), "Ссылка 'Contact Us' не отображается."
    browser.implicitly_wait(0)


def test_home_icon_catalog(browser, base_url):
    browser.implicitly_wait(5)
    browser.get(f"{base_url}/en-gb/catalog/desktops")

    icon_element = browser.find_element(By.CSS_SELECTOR, ".fa-home")

    assert icon_element.is_displayed()

    browser.implicitly_wait(0)


def test_mac_price(browser, base_url):
    browser.get(f"{base_url}/en-gb/product/desktops/mac/imac")

    locator = (By.XPATH, "//li[contains(text(), 'Ex Tax: ')]")

    wait = WebDriverWait(browser, 10)
    price_element = wait.until(EC.visibility_of_element_located(locator))

    full_text = price_element.text

    try:
        price_string = full_text.replace("Ex Tax: ", "").replace("$", "")
        price_value = float(price_string)
    except ValueError:
        pytest.fail(f"Не удалось преобразовать цену в число: '{full_text}'")

    assert price_value > 0, (
        f"Цена товара некорректна (меньше или равна нулю): {price_value}"
    )

    print(f"Цена Ex Tax успешно проверена: ${price_value}")
    browser.quit()


def test_login_admin(browser, base_url):
    wait = WebDriverWait(browser, 10)
    browser.get(f"{base_url}/administration/")

    wait.until(EC.visibility_of_element_located((By.ID, "input-username"))).send_keys(
        "user"
    )
    browser.find_element(By.ID, "input-password").send_keys("bitnami")

    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    profile_link = wait.until(EC.presence_of_element_located((By.ID, "nav-profile")))
    assert profile_link.is_displayed(), (
        "Админ-панель не загрузилась или профиль не виден"
    )

    try:
        alert_close_btn = WebDriverWait(browser, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".alert-success .btn-close"))
        )
        alert_close_btn.click()
        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
    except:
        pass

    logout_selector = "//a[contains(@href, 'route=common/logout')]"

    try:
        logout_link = wait.until(
            EC.presence_of_element_located((By.XPATH, logout_selector))
        )

        browser.execute_script("arguments[0].click();", logout_link)
    except Exception as e:
        pytest.fail(f"Не удалось найти или нажать кнопку Logout: {e}")

    username_field_after = wait.until(
        EC.visibility_of_element_located((By.ID, "input-username"))
    )
    password_field_after = browser.find_element(By.ID, "input-password")

    assert username_field_after.is_displayed(), (
        "Поле Username не появилось после выхода"
    )
    assert password_field_after.is_displayed(), (
        "Поле Password не появилось после выхода"
    )
    assert "route=common/login" in browser.current_url, (
        "URL не соответствует странице логина"
    )


def test_registration(browser, base_url):
    browser.implicitly_wait(3)
    browser.get(f"{base_url}/index.php?route=account/register")

    browser.find_element(By.ID, "input-firstname").send_keys("user1")
    browser.find_element(By.ID, "input-lastname").send_keys("lastname1")
    browser.find_element(By.ID, "input-email").send_keys("test@mail.ru")
    browser.find_element(By.ID, "input-password").send_keys("password1")
    browser.find_element(By.CSS_SELECTOR, 'input[name="agree"]').click()

    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    expected_text = "Your Account Has Been Created!"

    selector = f"//h1[contains(text(), '{expected_text}')]"

    element = browser.find_element(By.XPATH, selector)

    assert element.is_displayed(), (
        f"Элемент с текстом '{expected_text}' не отображается или не найден."
    )
    browser.quit()


def test_currency_switch(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 10)

    price_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".price-new"))
    )
    initial_price_text = price_element.text
    initial_currency_symbol = initial_price_text[0]

    assert initial_currency_symbol != "€", (
        "Изначальная валюта уже Euro, тест не имеет смысла."
    )

    currency_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.dropdown-toggle[data-bs-toggle='dropdown']")
        )
    )
    currency_button.click()

    euro_link_selector = "//a[contains(text(), 'Euro')]"
    euro_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, euro_link_selector))
    )
    browser.execute_script("arguments[0].click();", euro_link)

    wait.until(
        lambda driver: driver.find_element(By.CSS_SELECTOR, ".price-new").text
        != initial_price_text
    )

    new_price_element = browser.find_element(By.CSS_SELECTOR, ".price-new")
    new_price_text = new_price_element.text
    new_currency_symbol = new_price_text[-1]

    assert new_currency_symbol == "€", (
        f"Символ валюты не изменился на Euro. Получили: {new_currency_symbol}"
    )


def test_currency_switch_catalog(browser, base_url):
    browser.get(f"{base_url}/en-gb/product/desktops/mac/imac")
    wait = WebDriverWait(browser, 10)

    price_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".price-new"))
    )
    initial_price_text = price_element.text
    initial_currency_symbol = initial_price_text[0]

    assert initial_currency_symbol != "€", (
        "Изначальная валюта уже Euro, тест не имеет смысла."
    )

    currency_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.dropdown-toggle[data-bs-toggle='dropdown']")
        )
    )
    currency_button.click()

    euro_link_selector = "//a[contains(text(), 'Euro')]"
    euro_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, euro_link_selector))
    )
    browser.execute_script("arguments[0].click();", euro_link)

    wait.until(
        lambda driver: driver.find_element(By.CSS_SELECTOR, ".price-new").text
        != initial_price_text
    )

    new_price_element = browser.find_element(By.CSS_SELECTOR, ".price-new")
    new_price_text = new_price_element.text
    new_currency_symbol = new_price_text[-1]

    assert new_currency_symbol == "€", (
        f"Символ валюты не изменился на Euro. Получили: {new_currency_symbol}"
    )


def test_add_to_cart(browser, base_url):
    browser.get(f"{base_url}/en-gb/catalog/component/monitor")

    wait = WebDriverWait(browser, 10)

    add_buttons = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button[formaction*='checkout/cart.add']")
        )
    )

    assert len(add_buttons) >= 2, (
        f"На странице найдено меньше 2-х кнопок корзины. Найдено: {len(add_buttons)}"
    )

    second_button = add_buttons[1]

    browser.execute_script("arguments[0].scrollIntoView();", second_button)

    second_button.click()

    close_alert_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".alert-success .btn-close"))
    )
    close_alert_button.click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))

    cart_button_selector = "button.dropdown-toggle.btn-block"
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, cart_button_selector), "1 item(s)"
        )
    )

    cart_button = browser.find_element(By.CSS_SELECTOR, cart_button_selector)
    cart_button.click()

    product_link_xpath = "//a[text()='Samsung SyncMaster 941BW']"

    product_in_cart = wait.until(
        EC.visibility_of_element_located((By.XPATH, product_link_xpath))
    )

    assert product_in_cart.is_displayed(), "Товар не найден в раскрытом меню корзины"
