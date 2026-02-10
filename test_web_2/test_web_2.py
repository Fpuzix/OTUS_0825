from pages.home_page import HomePage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.admin_products_page import AdminProductsPage
from pages.registration_page import RegistrationPage
from pages.currency_page import CurrencyPage


# Главная
def test_home_page_logo(browser, base_url):
    assert HomePage(browser).open(base_url).logo_displayed(), "Лого не найден"


def test_banner_displayed(browser, base_url):
    assert HomePage(browser).open(base_url).banner_displayed(), "Баннер не найден"


def test_cart_button(browser, base_url):
    assert HomePage(browser).open(base_url).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


def test_good_button(browser, base_url):
    assert HomePage(browser).open(base_url).macbook_img_displayed(), (
        "Кнопка добавления товара не найдена"
    )


def test_contact_us(browser, base_url):
    assert HomePage(browser).open(base_url).contact_us_displayed(), (
        "Контакты не найдены"
    )


# Каталог
def test_catalog_page_logo(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).logo_displayed(), (
        "Лого на странице каталога не найдено"
    )


def test_fa_home_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


def test_cart_icon_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).cart_icon_displayed(), (
        "Иконка корзины не найдена"
    )


def test_page_active_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).pages_info_displayed(), (
        "Отображение страниц не найдено"
    )


def test_footer_link_displayed(browser, url_catalog):
    assert CatalogPage(browser).open(url_catalog).footer_link_displayed(), (
        "Ссылка футора не найдена"
    )


# Карточка товара
def test_good_page_logo(browser, url_goods):
    assert ProductPage(browser).open(url_goods).logo_displayed(), (
        "Лого на карточке товара не найдено"
    )


def test_good_page_fa_home_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


def test_good_page_search_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).search_displayed(), "Поиск не найден"


def test_good_page_btn_cart_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


def test_good_page_footer_link_displayed(browser, url_goods):
    assert ProductPage(browser).open(url_goods).footer_link_displayed(), (
        "Ссылка в футоре не найдена"
    )


# Страница логина в админку (/administration)
def test_adm_page_logo(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).logo_displayed(), (
        "Лого на страницы админ. не найден"
    )


def test_adm_page_fa_home_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).lock_icon_displayed(), (
        "Иконка замка не найдена"
    )


def test_adm_page_username_displayed(browser, url_administration):
    assert (
        AdminLoginPage(browser).open(url_administration).username_field_displayed()
    ), "Поле ввода username не найдено"


def test_adm_page_btn_submit_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).submit_button_displayed(), (
        "Кнопка Login не найдена"
    )


def test_adm_page_user_ic_displayed(browser, url_administration):
    assert AdminLoginPage(browser).open(url_administration).user_icon_displayed(), (
        "Иконка пользователя не найдена"
    )


# Страница регистрации пользователя (/index.php?route=account/register)
def test_reg_page_logo(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).logo_displayed(), (
        "Лого на странице регистрации пользователя не найдена"
    )


def test_reg_page_fa_home_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).home_icon_displayed(), (
        "Иконка дом не найдена"
    )


def test_reg_page_search_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).search_displayed(), (
        "Строка поиска не найдена"
    )


def test_reg_page_btn_cart_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).cart_button_displayed(), (
        "Кнопка корзины не найдена"
    )


def test_reg_page_user_ic_displayed(browser, url_registration):
    assert RegistrationPage(browser).open(url_registration).user_icon_displayed(), (
        "Иконка пользователя не найдена"
    )


# Сценарии
def test_home_icon_catalog(browser, url_catalog):
    CatalogPage(browser).open(url_catalog).home_icon_present()


def test_mac_price(browser, url_goods):
    ProductPage(browser).open(url_goods).assert_ex_tax_price_positive()


def test_add_random_to_cart(browser, url_catalog):
    CatalogPage(browser).open(
        url_catalog
    ).add_random_product_to_cart_and_assert_in_dropdown()


def test_currency_switch_home(browser, base_url):
    HomePage(browser).open(base_url).switch_currency_to_euro_and_assert()


def test_currency_switch_catalog(browser, url_goods):
    ProductPage(browser).open(url_goods).switch_currency_to_euro_and_assert()


def test_login_admin(browser, url_administration):
    page = AdminLoginPage(browser).open(url_administration)
    page.login("user", "bitnami")
    page.logout_and_assert_back_to_login()


def test_registration(browser, url_registration):
    RegistrationPage(browser).open(
        url_registration
    ).register_simple_and_assert_created()


# ________ ДОП СЦЕНАРИИ_____


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


def test_delete_product_admin(browser, url_administration):
    AdminLoginPage(browser).open(url_administration).login("user", "bitnami")

    products = AdminProductsPage(browser)
    products.open_products_list()
    products.delete_product_by_name("My New Product 2026")


def test_register_new_user(browser, url_registration):
    RegistrationPage(browser).open(
        url_registration
    ).register_new_user_and_assert_success()


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
