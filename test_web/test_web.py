import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import wait_element
from selenium.webdriver import ActionChains
import pytest


# Главная
def test_home_page_logo(browser):
    success = browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()
    assert success, "Лого не найден"


def test_banner_displayed(browser):
    success = browser.find_element(
        By.CSS_SELECTOR, 'img[alt="iPhone 6"]'
    ).is_displayed()
    assert success, "Баннер не найден"


def test_cart_button(browser):
    success = browser.find_element(
        By.XPATH, '//button[contains(., "item(s)")]'
    ).is_displayed()
    assert success, "Кнопка корзины не найдена"


def test_good_button(browser):
    success = browser.find_element(By.CSS_SELECTOR, 'img[alt="MacBook"]').is_displayed()
    assert success, "Кнопка добавления товара не найдена"


def test_contact_us(browser):
    success = browser.find_element(By.XPATH, '//a[text()="Contact Us"]').is_displayed()
    assert success, "Контакты не найдены"


# Каталог
def test_catalog_page_logo(browser, url_catalog):
    browser.get(url_catalog)
    success = browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()
    assert success, "Лого на странице каталога не найдено"


def test_fa_home_displayed(browser, url_catalog):
    browser.get(url_catalog)
    success = browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()
    assert success, "Иконка дом не найдена"


def test_cart_icon_displayed(browser, url_catalog):
    browser.get(url_catalog)
    success = browser.find_element(
        By.CSS_SELECTOR, ".fa-solid.fa-cart-shopping"
    ).is_displayed()
    assert success, "Иконка корзины не найдена"


def test_page_active_displayed(browser, url_catalog):
    browser.get(url_catalog)
    success = browser.find_element(
        By.CSS_SELECTOR, "div.col-sm-6.text-end"
    ).is_displayed()
    assert success, "Отображение страниц не найдено"


def test_footer_link_displayed(browser, url_catalog):
    browser.get(url_catalog)
    success = browser.find_element(By.LINK_TEXT, "OpenCart").is_displayed()
    assert success, "Ссылка футора не найдена"


# Карточку товара
def test_good_page_logo(browser, url_goods):
    browser.get(url_goods)
    success = browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()
    assert success, "Лого на карточке товара не найдено"


def test_good_page_fa_home_displayed(browser, url_goods):
    browser.get(url_goods)
    success = browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()
    assert success, "Иконка дом не найдена"


def test_good_page_search_displayed(browser, url_goods):
    browser.get(url_goods)
    success = browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Search"]'
    ).is_displayed()
    assert success, "Поиск не найден"


def test_good_page_btn_cart_displayed(browser, url_goods):
    browser.get(url_goods)
    success = browser.find_element(By.ID, "button-cart").is_displayed()
    assert success, "Кнопка корзины не найдена"


def test_good_page_footer_link_displayed(browser, url_goods):
    browser.get(url_goods)
    success = browser.find_element(By.LINK_TEXT, "OpenCart").is_displayed()
    assert success, "Ссылка в футоре не найдена"


# Страницу логина в админку /administration
def test_adm_page_logo(browser, url_administration):
    browser.get(url_administration)
    success = browser.find_element(
        By.CSS_SELECTOR, "img[title='OpenCart']"
    ).is_displayed()
    assert success, "Лого на страницы админ. не найден"


def test_adm_page_fa_home_displayed(browser, url_administration):
    browser.get(url_administration)
    success = browser.find_element(By.CSS_SELECTOR, ".fa-lock").is_displayed()
    assert success, "Иконка дом не найдена"


def test_adm_page_username_displayed(browser, url_administration):
    browser.get(url_administration)
    success = browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Username"]'
    ).is_displayed()
    assert success, "Поле ввода юзернейм не найдено"


def test_adm_page_btn_cart_displayed(browser, url_administration):
    browser.get(url_administration)
    success = browser.find_element(
        By.CSS_SELECTOR, "button[type='submit'].btn-primary"
    ).is_displayed()
    assert success, "Кнопка корзины не найдена"


def test_adm_page_user_ic_displayed(browser, url_administration):
    browser.get(url_administration)
    success = browser.find_element(By.CSS_SELECTOR, ".fa-user").is_displayed()
    assert success, "Иконка пользователя не найдена"


# Страницу регистрации пользователя (/index.php?route=account/register)
def test_reg_page_logo(browser, url_registration):
    browser.get(url_registration)
    success = browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()
    assert success, "Лого на странице регистрации пользователя не найдена"


def test_reg_page_fa_home_displayed(browser, url_registration):
    browser.get(url_registration)
    success = browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()
    assert success, "Иконка дом не найдена"


def test_reg_page_search_displayed(browser, url_registration):
    browser.get(url_registration)
    success = browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Search"]'
    ).is_displayed()
    assert success, "Строка поиска не найдена"


def test_reg_page_btn_cart_displayed(browser, url_registration):
    browser.get(url_registration)
    success = browser.find_element(
        By.CSS_SELECTOR, "button[data-bs-toggle='dropdown'].btn-block"
    ).is_displayed()
    assert success, "Кнопка корзины не найдена"


def test_reg_page_user_ic_displayed(browser, url_registration):
    browser.get(url_registration)
    success = browser.find_element(By.CSS_SELECTOR, ".fa-user").is_displayed()
    assert success, "Иконка пользователя не найдена"


# Сценарии
def test_home_icon_catalog(browser, url_catalog):
    browser.get(url_catalog)

    icon = wait_element(browser, (By.CSS_SELECTOR, ".fa-home"), name="Иконка дома")

    assert icon is not None, "Иконка 'Домой' не найдена в каталоге"
    assert icon.is_displayed(), "Иконка 'Домой' найдена, но не отображается"


def test_mac_price(browser, url_goods):
    browser.get(url_goods)

    price_element = wait_element(
        browser, (By.XPATH, "//li[contains(text(), 'Ex Tax: ')]"), name="Цена Ex Tax"
    )

    assert price_element is not None, "Элемент с ценой Ex Tax не найден на странице"

    clean_price = "".join(c for c in price_element.text if c.isdigit() or c == ".")

    try:
        price_value = float(clean_price)
    except ValueError:
        price_value = 0

    assert price_value > 0, f"Цена товара некорректна: {price_value}"


def test_add_random_to_cart(browser, url_catalog):
    browser.get(url_catalog)

    btns = browser.find_elements(
        By.CSS_SELECTOR, "button[formaction*='checkout/cart.add']"
    )
    assert len(btns) > 0, "На странице нет товаров для добавления"

    random_index = random.randint(0, len(btns) - 1)
    target_button = btns[random_index]

    product_card = target_button.find_element(
        By.XPATH, "./ancestor::div[@class='product-thumb']"
    )
    product_name = product_card.find_element(By.CSS_SELECTOR, "h4 a").text

    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", target_button
    )
    target_button.click()

    if "route=product/product" in browser.current_url:
        btn_on_page = wait_element(
            browser, (By.ID, "button-cart"), name="Кнопка в карточке"
        )
        if btn_on_page:
            btn_on_page.click()

    close_btn = wait_element(
        browser, (By.CSS_SELECTOR, ".alert-success .btn-close"), name="Крестик алерта"
    )
    if close_btn:
        close_btn.click()

    cart_btn_locator = (By.CSS_SELECTOR, "button.btn-inverse")
    wait_element(browser, cart_btn_locator, name="Обновленная кнопка корзины")

    cart_button = browser.find_element(*cart_btn_locator)
    browser.execute_script("arguments[0].click();", cart_button)

    product_in_cart = wait_element(
        browser,
        (By.XPATH, f"//div[@id='header-cart']//a[contains(text(), '{product_name}')]"),
        name=f"Товар {product_name} в корзине",
    )

    assert product_in_cart is not None, (
        f"Товар '{product_name}' не найден в корзине после добавления"
    )


def test_currency_switch_home(browser):
    price_locator = (By.CSS_SELECTOR, ".price-new")

    price_el = wait_element(browser, price_locator, name="Старая цена")
    assert price_el is not None, "Цена не найдена на главной странице"
    initial_text = price_el.text

    browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()

    euro_link = wait_element(
        browser, (By.XPATH, "//a[contains(., 'Euro')]"), name="Ссылка Euro"
    )
    assert euro_link is not None, "Валюта Euro не найдена в списке"

    browser.execute_script("arguments[0].click();", euro_link)

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(*price_locator).text != initial_text
    )

    new_price_text = browser.find_element(*price_locator).text
    assert "€" in new_price_text, f"Ожидался символ €, но получили: {new_price_text}"


def test_currency_switch_catalog(browser, url_goods):
    browser.get(url_goods)
    price_locator = (By.CSS_SELECTOR, ".price-new")

    price_el = wait_element(browser, price_locator, name="Старая цена")
    assert price_el is not None, "Элемент цены не найден на странице"
    initial_text = price_el.text

    browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()

    euro_link = wait_element(
        browser, (By.XPATH, "//a[contains(., 'Euro')]"), name="Ссылка Euro"
    )
    assert euro_link is not None, "Ссылка выбора Euro не найдена"

    browser.execute_script("arguments[0].click();", euro_link)

    WebDriverWait(browser, 10).until_not(
        EC.text_to_be_present_in_element(price_locator, initial_text)
    )

    new_price_text = browser.find_element(*price_locator).text
    assert "€" in new_price_text, f"Ожидался символ €, но получили: {new_price_text}"


def test_login_admin(browser, url_administration):
    browser.get(url_administration)

    user_field = wait_element(browser, (By.ID, "input-username"), name="Поле логина")
    user_field.send_keys("user")

    browser.find_element(By.ID, "input-password").send_keys("bitnami")

    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    profile_icon = wait_element(browser, (By.ID, "nav-profile"), name="Профиль админа")
    assert profile_icon is not None, "Не удалось войти в админ-панель"

    logout_link = wait_element(
        browser,
        (By.XPATH, "//a[contains(@href, 'route=common/logout')]"),
        name="Кнопка выхода",
    )

    browser.execute_script("arguments[0].click();", logout_link)

    username_after = wait_element(
        browser, (By.ID, "input-username"), name="Поле логина после выхода"
    )

    assert username_after is not None, "После выхода страница логина не загрузилась"
    assert username_after.is_displayed()


def test_registration(browser, url_registration):
    browser.get(url_registration)

    wait_element(browser, (By.ID, "input-firstname"), name="Имя").send_keys("Ivan")
    wait_element(browser, (By.ID, "input-lastname"), name="Фамилия").send_keys("Ivanov")

    email = f"test{int(time.time())}@mail.ru"
    wait_element(browser, (By.ID, "input-email"), name="Email").send_keys(email)
    wait_element(browser, (By.ID, "input-password"), name="Пароль").send_keys(
        "password123"
    )

    agree = wait_element(browser, (By.NAME, "agree"), name="Чекбокс соглашения")
    browser.execute_script("arguments[0].click();", agree)

    submit_button = wait_element(
        browser, (By.CSS_SELECTOR, "button[type='submit']"), name="Кнопка"
    )

    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", submit_button
    )
    submit_button.click()

    success = wait_element(
        browser,
        (By.XPATH, "//h1[contains(text(), 'Created')]"),
        name="Заголовок успеха",
        timeout=10,
    )

    assert success is not None, "Заголовок об успешной регистрации не найден"
    assert "Created" in success.text


# ________ ДОП СЦЕНАРИИ_____


def test_add_new_product_admin(browser, url_administration):
    browser.get(url_administration)

    user_field = wait_element(browser, (By.ID, "input-username"), name="Поле логина")
    user_field.clear()
    user_field.send_keys("user")

    pass_field = browser.find_element(By.ID, "input-password")
    pass_field.clear()
    pass_field.send_keys("bitnami")

    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    wait_element(browser, (By.ID, "nav-profile"), name="Профиль админа")

    catalog_menu = wait_element(
        browser, (By.CSS_SELECTOR, "#menu-catalog > a"), name="Меню Catalog"
    )
    catalog_menu.click()

    products_link = wait_element(
        browser, (By.LINK_TEXT, "Products"), name="Подменю Products"
    )
    browser.execute_script("arguments[0].click();", products_link)

    add_new_btn = wait_element(
        browser,
        (
            By.CSS_SELECTOR,
            "a[href*='catalog/product.form'], a[href*='catalog/product|add']",
        ),
        name="Кнопка Добавить новый",
    )
    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", add_new_btn
    )
    browser.execute_script("arguments[0].click();", add_new_btn)

    time.sleep(1)

    name_field = wait_element(browser, (By.ID, "input-name-1"), name="Product Name")
    name_field.clear()
    name_field.send_keys("My New Product 2026")

    meta_field = wait_element(
        browser, (By.ID, "input-meta-title-1"), name="Meta Tag Title"
    )
    meta_field.clear()
    meta_field.send_keys("Product Meta Title")

    tab_data = wait_element(browser, (By.LINK_TEXT, "Data"), name="Вкладка Data")
    browser.execute_script("arguments[0].click();", tab_data)

    time.sleep(0.5)

    model_field = wait_element(browser, (By.ID, "input-model"), name="Model")
    model_field.clear()
    model_field.send_keys("Model-2026-Test")

    tab_seo = wait_element(browser, (By.LINK_TEXT, "SEO"), name="Вкладка SEO")
    browser.execute_script("arguments[0].click();", tab_seo)

    time.sleep(0.8)

    seo_field = wait_element(
        browser,
        (By.CSS_SELECTOR, "input[name='product_seo_url[0][1]']"),
        name="SEO Keyword Field",
    )

    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", seo_field)
    seo_field.clear()
    seo_field.send_keys(f"test-product-{int(time.time())}")

    browser.execute_script("arguments[0].focus();", tab_seo)

    save_button = wait_element(
        browser,
        (By.CSS_SELECTOR, "button[form='form-product']"),
        name="Кнопка Сохранить",
    )

    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", save_button
    )
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", save_button)

    success_alert = wait_element(
        browser,
        (By.CSS_SELECTOR, ".alert-success, .alert-dismissible"),
        name="Алерт успеха",
        timeout=10,
    )

    if success_alert is None:
        errors = browser.find_elements(By.CSS_SELECTOR, ".text-danger, .is-invalid")
        error_texts = [err.text for err in errors if err.text]
        assert success_alert is not None, (
            f"Товар не сохранен! Найдены ошибки: {error_texts}"
        )

    assert (
        "Success" in success_alert.text
        or "You have modified products" in success_alert.text
    )


def test_delete_product_admin(browser, url_administration):
    browser.get(url_administration)

    user_field = wait_element(browser, (By.ID, "input-username"), name="Поле логина")
    user_field.clear()
    user_field.send_keys("user")

    pass_field = browser.find_element(By.ID, "input-password")
    pass_field.clear()
    pass_field.send_keys("bitnami")

    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    wait_element(browser, (By.ID, "nav-profile"), name="Профиль админа")

    catalog_menu = wait_element(browser, (By.CSS_SELECTOR, "#menu-catalog > a"))
    catalog_menu.click()
    products_link = wait_element(browser, (By.LINK_TEXT, "Products"))
    browser.execute_script("arguments[0].click();", products_link)

    product_name = "My New Product 2026"

    filter_name = wait_element(browser, (By.ID, "input-name"), name="Фильтр по имени")
    filter_name.send_keys(product_name)

    filter_button = browser.find_element(By.ID, "button-filter")
    filter_button.click()
    time.sleep(1)

    product_checkbox = wait_element(
        browser,
        (
            By.XPATH,
            f"//td[contains(text(), '{product_name}')]/preceding-sibling::td/input[@type='checkbox']",
        ),
        name="Чекбокс товара",
    )
    if not product_checkbox.is_selected():
        product_checkbox.click()

    delete_button = wait_element(
        browser,
        (By.CSS_SELECTOR, "button[data-oc-action*='product|delete'], .btn-danger"),
        name="Кнопка Удалить",
    )
    delete_button.click()

    WebDriverWait(browser, 5).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()

    success_alert = wait_element(
        browser, (By.CSS_SELECTOR, ".alert-success"), name="Алерт успеха удаления"
    )

    assert "Success" in success_alert.text or "modified" in success_alert.text

    no_results = browser.find_elements(
        By.XPATH, f"//td[contains(text(), '{product_name}')]"
    )
    assert len(no_results) == 0, "Товар всё еще отображается в списке после удаления!"


def test_register_new_user(browser, url_registration):
    browser.get(url_registration)

    wait_element(browser, (By.ID, "input-firstname")).send_keys("Ivan")
    wait_element(browser, (By.ID, "input-lastname")).send_keys("Testerov")

    email = f"test_user_{int(time.time())}@example.com"
    browser.find_element(By.ID, "input-email").send_keys(email)

    telephones = browser.find_elements(By.ID, "input-telephone")
    if telephones:
        telephones[0].send_keys("1234567890")

    browser.find_element(By.ID, "input-password").send_keys("test_password_2026")

    agree_check = browser.find_element(By.NAME, "agree")
    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", agree_check
    )
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", agree_check)

    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].click();", submit_button)

    time.sleep(2)

    header_element = wait_element(browser, (By.CSS_SELECTOR, "h1"))
    current_h1 = header_element.text

    if current_h1 == "Register Account":
        error_elements = browser.find_elements(
            By.CSS_SELECTOR, ".text-danger, .alert-danger, .invalid-feedback"
        )
        error_list = [err.text for err in error_elements if err.text]

        if not error_list:
            pytest.fail(
                "Форма не была отправлена (ошибок нет, но мы всё еще на странице регистрации)."
            )
        else:
            pytest.fail(f"Регистрация не удалась. Ошибки: {error_list}")

    assert current_h1 == "Your Account Has Been Created!"


def test_switch_all_currencies(browser, base_url):
    browser.get(base_url)

    currencies = [("Euro", "€"), ("Pound Sterling", "£"), ("US Dollar", "$")]

    for currency_name, symbol in currencies:
        dropdown = wait_element(
            browser, (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
        )
        browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", dropdown
        )
        dropdown.click()

        time.sleep(0.5)

        currency_option_xpath = f"//ul[@class='dropdown-menu show']//button[contains(text(), '{currency_name}')] | //ul[@class='dropdown-menu show']//a[contains(text(), '{currency_name}')] | //button[contains(@name, '{currency_name[:3].upper()}')]"

        try:
            btn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, currency_option_xpath))
            )

            btn.click()
        except:
            btn = browser.find_element(By.XPATH, currency_option_xpath)
            browser.execute_script("arguments[0].click();", btn)

        time.sleep(1.5)

        cart_val = wait_element(browser, (By.CSS_SELECTOR, "#header-cart button")).text

        product_price = browser.find_element(By.CSS_SELECTOR, ".price-new, .price").text

        assert symbol in cart_val or symbol in product_price, (
            f"Валюта {currency_name} не применилась! Ожидали {symbol}. В корзине: {cart_val}, в товаре: {product_price}"
        )

        print(f"Успешно переключено на {currency_name} ({symbol})")
