import allure

from pages.home_page import HomePage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.admin_products_page import AdminProductsPage
from pages.registration_page import RegistrationPage
from pages.currency_page import CurrencyPage


# Главная
@allure.title("test_home_page_logo")
@allure.suite("OpenCart UI")
@allure.feature("Home")
@allure.story("UI elements")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("smoke", "ui")
def test_home_page_logo(browser, base_url):
    assert HomePage(browser).open(base_url).logo_displayed(), "Лого не найден"


@allure.title("test_banner_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Home")
@allure.story("UI elements")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("smoke", "ui")
def test_banner_displayed(browser, base_url):
    assert HomePage(browser).open(base_url).banner_displayed(), "Баннер не найден"


@allure.title("test_cart_button")
@allure.suite("OpenCart UI")
@allure.feature("Home")
@allure.story("UI elements")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("smoke", "ui")
def test_cart_button(browser, base_url):
    assert HomePage(browser).open(base_url).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


@allure.title("test_good_button")
@allure.suite("OpenCart UI")
@allure.feature("Home")
@allure.story("UI elements")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("smoke", "ui")
def test_good_button(browser, base_url):
    assert HomePage(browser).open(base_url).macbook_img_displayed(), (
        "Кнопка добавления товара не найдена"
    )


@allure.title("test_contact_us")
@allure.suite("OpenCart UI")
@allure.feature("Home")
@allure.story("UI elements")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("smoke", "ui")
def test_contact_us(browser, base_url):
    assert HomePage(browser).open(base_url).contact_us_displayed(), (
        "Контакты не найдены"
    )


# Каталог
@allure.title("test_catalog_page_logo")
@allure.suite("OpenCart UI")
@allure.feature("Catalog")
@allure.story("Catalog browsing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_catalog_page_logo(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).logo_displayed(), (
        "Лого на странице каталога не найдено"
    )


@allure.title("test_fa_home_displayed")
@allure.suite("OpenCart UI")
@allure.feature("General")
@allure.story("Checks")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke")
def test_fa_home_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


@allure.title("test_cart_icon_displayed")
@allure.suite("OpenCart UI")
@allure.feature("General")
@allure.story("Checks")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke")
def test_cart_icon_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).cart_icon_displayed(), (
        "Иконка корзины не найдена"
    )


@allure.title("test_page_active_displayed")
@allure.suite("OpenCart UI")
@allure.feature("General")
@allure.story("Checks")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke")
def test_page_active_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).pages_info_displayed(), (
        "Отображение страниц не найдено"
    )


@allure.title("test_footer_link_displayed")
@allure.suite("OpenCart UI")
@allure.feature("General")
@allure.story("Checks")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke")
def test_footer_link_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).footer_link_displayed(), (
        "Ссылка футора не найдена"
    )


# Карточка товара
@allure.title("test_good_page_logo")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_good_page_logo(browser, url_goods):
    assert ProductPage(browser).open(url_goods).logo_displayed(), (
        "Лого на карточке товара не найдено"
    )


@allure.title("test_good_page_fa_home_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke", "ui")
def test_good_page_fa_home_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


@allure.title("test_good_page_search_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke", "ui")
def test_good_page_search_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).search_displayed(), "Поиск не найден"


@allure.title("test_good_page_btn_cart_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke", "ui")
def test_good_page_btn_cart_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


@allure.title("test_good_page_footer_link_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("smoke", "ui")
def test_good_page_footer_link_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).footer_link_displayed(), (
        "Ссылка в футоре не найдена"
    )


# Страница логина в админку (/administration)
@allure.title("test_adm_page_logo")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("admin", "regression")
def test_adm_page_logo(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).logo_displayed(), (
        "Лого на страницы админ. не найден"
    )


@allure.title("test_adm_page_fa_home_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("admin", "regression")
def test_adm_page_fa_home_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).lock_icon_displayed(), (
        "Иконка замка не найдена"
    )


@allure.title("test_adm_page_username_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("admin", "regression")
def test_adm_page_username_displayed(browser, url_administration):
    assert (
        AdminLoginPage(browser).open(url_administration).username_field_displayed()
    ), "Поле ввода username не найдено"


@allure.title("test_adm_page_btn_submit_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("admin", "regression")
def test_adm_page_btn_submit_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).submit_button_displayed(), (
        "Кнопка Login не найдена"
    )


@allure.title("test_adm_page_user_ic_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("admin", "regression")
def test_adm_page_user_ic_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).user_icon_displayed(), (
        "Иконка пользователя не найдена"
    )


# Страница регистрации пользователя (/index.php?route=account/register)
@allure.title("test_reg_page_logo")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_reg_page_logo(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).logo_displayed(), (
        "Лого на странице регистрации пользователя не найдена"
    )


@allure.title("test_reg_page_fa_home_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_reg_page_fa_home_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


@allure.title("test_reg_page_search_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_reg_page_search_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).search_displayed(), (
        "Строка поиска не найдена"
    )


@allure.title("test_reg_page_btn_cart_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_reg_page_btn_cart_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


@allure.title("test_reg_page_user_ic_displayed")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_reg_page_user_ic_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).user_icon_displayed(), (
        "Иконка пользователя не найдена"
    )


# Сценарии
@allure.title("test_home_icon_catalog")
@allure.suite("OpenCart UI")
@allure.feature("Catalog")
@allure.story("Catalog browsing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_home_icon_catalog(browser, url_catalog):
    CatalogPage(browser).open(url_catalog).home_icon_present()


@allure.title("test_mac_price")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_mac_price(browser, url_goods):
    ProductPage(browser).open(url_goods).assert_ex_tax_price_positive()


@allure.title("test_add_random_to_cart")
@allure.suite("OpenCart UI")
@allure.feature("Catalog")
@allure.story("Catalog browsing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_add_random_to_cart(browser, url_catalog):
    CatalogPage(browser).open(
        url_catalog
    ).add_random_product_to_cart_and_assert_in_dropdown()


@allure.title("test_currency_switch_home")
@allure.suite("OpenCart UI")
@allure.feature("Currency")
@allure.story("Switch currency")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "currency")
def test_currency_switch_home(browser, base_url):
    HomePage(browser).open(base_url).switch_currency_to_euro_and_assert()


@allure.title("test_currency_switch_catalog")
@allure.suite("OpenCart UI")
@allure.feature("Catalog")
@allure.story("Catalog browsing")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_currency_switch_catalog(browser, url_goods):
    ProductPage(browser).open(url_goods).switch_currency_to_euro_and_assert()


@allure.title("test_login_admin")
@allure.suite("OpenCart UI")
@allure.feature("Admin")
@allure.story("Admin panel")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("admin", "regression")
def test_login_admin(browser, url_administration):
    page = AdminLoginPage(browser).open(url_administration)
    page.login("user", "bitnami")
    page.logout_and_assert_back_to_login()


@allure.title("test_registration")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_registration(browser, url_registration):
    RegistrationPage(browser).open(
        url_registration
    ).register_simple_and_assert_created()


# ________ ДОП СЦЕНАРИИ_____


@allure.title("test_add_new_product_admin")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_add_new_product_admin(browser, url_administration):
    AdminLoginPage(browser).open(url_administration).login("user", "bitnami")

    products = AdminProductsPage(browser)
    products.open_products_list()
    products.add_new_product(
        name="My New Product 2026",
        meta_title="Product Meta Title",
        model="Model-2026-Test",
        seo_prefix="test-product",
    )


@allure.title("test_delete_product_admin")
@allure.suite("OpenCart UI")
@allure.feature("Product")
@allure.story("Product page")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression")
def test_delete_product_admin(browser, url_administration):
    AdminLoginPage(browser).open(url_administration).login("user", "bitnami")

    products = AdminProductsPage(browser)
    products.open_products_list()
    products.delete_product_by_name("My New Product 2026")


@allure.title("test_register_new_user")
@allure.suite("OpenCart UI")
@allure.feature("Registration")
@allure.story("Create account")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("regression", "auth")
def test_register_new_user(browser, url_registration):
    RegistrationPage(browser).open(
        url_registration
    ).register_new_user_and_assert_success()


@allure.title("test_switch_all_currencies")
@allure.suite("OpenCart UI")
@allure.feature("Currency")
@allure.story("Switch currency")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "currency")
def test_switch_all_currencies(browser, base_url):
    page = CurrencyPage(browser).open(base_url)

    currencies = [
        ("Euro", "€"),
        ("Pound Sterling", "£"),
        ("US Dollar", "$"),
    ]

    for currency_name, symbol in currencies:
        page.switch_currency(currency_name)
        page.assert_symbol_applied(symbol, currency_name)
