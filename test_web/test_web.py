import random
from selenium.webdriver.common.by import By


# Главная
def test_home_page_logo(browser):
    assert browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()


def test_banner_displayed(browser):
    assert browser.find_element(By.CSS_SELECTOR, 'img[alt="iPhone 6"]').is_displayed()


def test_cart_button(browser):
    assert browser.find_element(
        By.XPATH, '//button[contains(., "item(s)")]'
    ).is_displayed()


def test_good_button(browser):
    assert browser.find_element(By.CSS_SELECTOR, 'img[alt="MacBook"]').is_displayed()


def test_contact_us(browser):
    assert browser.find_element(By.XPATH, '//a[text()="Contact Us"]').is_displayed()


# Каталог
def test_catalog_page_logo(browser, url_catalog):
    browser.get(url_catalog)
    assert browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()


def test_fa_home_displayed(browser, url_catalog):
    browser.get(url_catalog)
    assert browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()


def test_cart_icon_displayed(browser, url_catalog):
    browser.get(url_catalog)
    assert browser.find_element(
        By.CSS_SELECTOR, ".fa-solid.fa-cart-shopping"
    ).is_displayed()


def test_page_active_displayed(browser, url_catalog):
    browser.get(url_catalog)
    assert browser.find_element(By.CSS_SELECTOR, "div.col-sm-6.text-end").is_displayed()


def test_footer_link_displayed(browser, url_catalog):
    browser.get(url_catalog)
    assert browser.find_element(By.LINK_TEXT, "OpenCart").is_displayed()


# Карточку товара
def test_good_page_logo(browser, url_goods):
    browser.get(url_goods)
    assert browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()


def test_good_page_fa_home_displayed(browser, url_goods):
    browser.get(url_goods)
    assert browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()


def test_good_page_search_displayed(browser, url_goods):
    browser.get(url_goods)
    assert browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Search"]'
    ).is_displayed()


def test_good_page_btn_cart_displayed(browser, url_goods):
    browser.get(url_goods)
    assert browser.find_element(By.ID, "button-cart").is_displayed()


def test_good_page_footer_link_displayed(browser, url_goods):
    browser.get(url_goods)
    assert browser.find_element(By.LINK_TEXT, "OpenCart").is_displayed()


# Страницу логина в админку /administration
def test_adm_page_logo(browser, url_administration):
    browser.get(url_administration)
    assert browser.find_element(By.CSS_SELECTOR, "img[title='OpenCart']").is_displayed()


def test_adm_page_fa_home_displayed(browser, url_administration):
    browser.get(url_administration)
    assert browser.find_element(By.CSS_SELECTOR, ".fa-lock").is_displayed()


def test_adm_page_username_displayed(browser, url_administration):
    browser.get(url_administration)
    assert browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Username"]'
    ).is_displayed()


def test_adm_page_btn_cart_displayed(browser, url_administration):
    browser.get(url_administration)
    assert browser.find_element(
        By.CSS_SELECTOR, "button[type='submit'].btn-primary"
    ).is_displayed()


def test_adm_page_user_ic_displayed(browser, url_administration):
    browser.get(url_administration)
    assert browser.find_element(By.CSS_SELECTOR, ".fa-user").is_displayed()


# Страницу регистрации пользователя (/index.php?route=account/register)
def test_reg_page_logo(browser, url_registration):
    browser.get(url_registration)
    assert browser.find_element(
        By.CSS_SELECTOR, "img[title='Your Store']"
    ).is_displayed()


def test_reg_page_fa_home_displayed(browser, url_registration):
    browser.get(url_registration)
    assert browser.find_element(By.CSS_SELECTOR, ".fas.fa-home").is_displayed()


def test_reg_page_search_displayed(browser, url_registration):
    browser.get(url_registration)
    assert browser.find_element(
        By.CSS_SELECTOR, 'input[placeholder="Search"]'
    ).is_displayed()


def test_reg_page_btn_cart_displayed(browser, url_registration):
    browser.get(url_registration)
    assert browser.find_element(
        By.CSS_SELECTOR, "button[data-bs-toggle='dropdown'].btn-block"
    ).is_displayed()


def test_reg_page_user_ic_displayed(browser, url_registration):
    browser.get(url_registration)
    assert browser.find_element(By.CSS_SELECTOR, ".fa-user").is_displayed()


# Сценарии
def test_home_icon_catalog(browser, url_catalog, wait_element):
    browser.get(url_catalog)
    icon = wait_element((By.CSS_SELECTOR, ".fa-home"), name="Иконка дома")
    assert icon is not None and icon.is_displayed()


def test_mac_price(browser, url_goods, wait_element):
    browser.get(url_goods)
    price_element = wait_element(
        (By.XPATH, "//li[contains(text(), 'Ex Tax: ')]"), name="Цена Ex Tax"
    )
    assert price_element is not None
    clean_price = "".join(c for c in price_element.text if c.isdigit() or c == ".")
    assert float(clean_price) > 0


def test_add_random_to_cart(browser, url_catalog, wait_element):
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
    print(f"Добавляем случайный товар: {product_name}")

    browser.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", target_button
    )
    target_button.click()

    close_btn = wait_element(
        (By.CSS_SELECTOR, ".alert-success .btn-close"), name="Крестик алерта"
    )
    if close_btn:
        close_btn.click()

    cart_btn_locator = (By.CSS_SELECTOR, "button.btn-inverse")
    wait_element(cart_btn_locator, name="Обновленная кнопка корзины")

    browser.find_element(*cart_btn_locator).click()

    product_in_cart = wait_element(
        (By.XPATH, f"//div[@id='header-cart']//a[text()='{product_name}']"),
        name=f"Товар {product_name} в корзине",
    )

    assert product_in_cart is not None, (
        f"Товар '{product_name}' не найден в корзине после добавления"
    )


def test_currency_switch_home(browser, wait_element):
    price_locator = (By.CSS_SELECTOR, ".price-new")
    initial_text = wait_element(price_locator).text

    browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()
    euro_link = wait_element((By.XPATH, "//a[contains(., 'Euro')]"), name="Ссылка Euro")
    browser.execute_script("arguments[0].click();", euro_link)

    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(*price_locator).text != initial_text
    )

    assert "€" in browser.find_element(*price_locator).text


def test_currency_switch_catalog(browser, url_goods, wait_element):
    browser.get(url_goods)
    price_locator = (By.CSS_SELECTOR, ".price-new")
    initial_text = wait_element(price_locator).text

    browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()
    euro_link = wait_element((By.XPATH, "//a[contains(., 'Euro')]"))
    browser.execute_script("arguments[0].click();", euro_link)

    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(browser, 10).until(
        lambda d: d.find_element(*price_locator).text != initial_text
    )
    assert "€" in browser.find_element(*price_locator).text


def test_login_admin(browser, url_administration, wait_element):
    browser.get(url_administration)

    wait_element((By.ID, "input-username")).send_keys("user")
    browser.find_element(By.ID, "input-password").send_keys("bitnami")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert wait_element((By.ID, "nav-profile"), name="Профиль админа") is not None

    logout_link = wait_element(
        (By.XPATH, "//a[contains(@href, 'logout')]"), name="Кнопка выхода"
    )
    browser.execute_script("arguments[0].click();", logout_link)

    assert (
        wait_element((By.ID, "input-username"), name="Поле логина после выхода")
        is not None
    )


def test_registration(browser, url_registration, wait_element):
    browser.get(url_registration)

    browser.find_element(By.ID, "input-firstname").send_keys("Ivan")
    browser.find_element(By.ID, "input-lastname").send_keys("Ivanov")

    import time

    email = f"test{int(time.time())}@mail.ru"
    browser.find_element(By.ID, "input-email").send_keys(email)
    browser.find_element(By.ID, "input-password").send_keys("password123")

    agree = browser.find_element(By.NAME, "agree")
    browser.execute_script("arguments[0].click();", agree)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    success = wait_element(
        (By.XPATH, "//h1[contains(., 'Created')]"), name="Заголовок успеха"
    )
    assert success is not None
