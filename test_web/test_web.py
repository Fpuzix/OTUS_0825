import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import wait_element


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
