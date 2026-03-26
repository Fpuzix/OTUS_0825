import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class AdminProductsPage(BasePage):
    # Левое меню
    MENU_CATALOG = (By.CSS_SELECTOR, "#menu-catalog > a")
    SUBMENU_PRODUCTS = (By.LINK_TEXT, "Products")

    # Список продуктов
    FILTER_NAME = (By.ID, "input-name")
    FILTER_BTN = (By.ID, "button-filter")

    # Кнопки
    ADD_NEW_BTN = (
        By.CSS_SELECTOR,
        "a[href*='catalog/product.form'], a[href*='catalog/product|add']",
    )

    # Delete-кнопка
    DELETE_BTN = (
        By.CSS_SELECTOR,
        "button[data-oc-action*='product|delete'], "
        "button[form='form-product'][formaction*='catalog/product.delete'], "
        "button.btn-danger[form='form-product']",
    )

    # Форма создания/редактирования
    NAME_FIELD = (By.ID, "input-name-1")
    META_FIELD = (By.ID, "input-meta-title-1")
    TAB_DATA = (By.LINK_TEXT, "Data")
    MODEL_FIELD = (By.ID, "input-model")
    TAB_SEO = (By.LINK_TEXT, "SEO")
    SEO_FIELD = (By.CSS_SELECTOR, "input[name='product_seo_url[0][1]']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[form='form-product']")

    # Алерты
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success, .alert-dismissible")
    SUCCESS_DELETE = (By.CSS_SELECTOR, ".alert-success")

    # Таблица
    TABLE_ROWS = (By.CSS_SELECTOR, "#form-product tbody tr")
    NO_RESULTS = (
        By.XPATH,
        "//form[@id='form-product']//tbody//td[contains(., 'No results') or contains(., 'Нет результатов')]",
    )

    @property
    def page_marker(self):
        return self.MENU_CATALOG

    def open_products_list(self):
        self.click(self.MENU_CATALOG, name="Меню Catalog")
        products_link = self.wait_visible(
            self.SUBMENU_PRODUCTS, name="Подменю Products"
        )
        self.js_click(products_link)

        self.wait_visible(self.FILTER_NAME, name="Фильтр по имени", timeout=10)
        return self

    def add_new_product(
        self, name: str, meta_title: str, model: str, seo_prefix: str = "test-product"
    ):
        self.click(self.ADD_NEW_BTN, name="Кнопка Add New")

        self.type(self.NAME_FIELD, name, name="Product Name")
        self.type(self.META_FIELD, meta_title, name="Meta Tag Title")

        self.click(self.TAB_DATA, name="Вкладка Data")
        self.type(self.MODEL_FIELD, model, name="Model")

        self.click(self.TAB_SEO, name="Вкладка SEO")
        seo_val = f"{seo_prefix}-{int(time.time())}"
        seo_field = self.wait_visible(self.SEO_FIELD, name="SEO Keyword Field")
        seo_field.clear()
        seo_field.send_keys(seo_val)

        self.click(self.SAVE_BUTTON, name="Кнопка Save")

        success_alert = self.wait_visible(
            self.SUCCESS_ALERT, name="Алерт успеха", timeout=10
        )
        assert ("Success" in success_alert.text) or (
            "modified" in success_alert.text
        ), f"Не нашли сообщение об успехе. Текст алерта: {success_alert.text}"
        return self

    def delete_product_by_name(self, product_name: str):
        self.type(self.FILTER_NAME, product_name, name="Фильтр по имени")
        self.click(self.FILTER_BTN, name="Кнопка Filter")

        WebDriverWait(self.driver, 20).until(
            lambda d: len(d.find_elements(*self.TABLE_ROWS)) > 0,
            message="Timeout: table rows not loaded after filter",
        )

        if self.driver.find_elements(*self.NO_RESULTS):
            raise AssertionError(
                f"Товар '{product_name}' не найден в админке после фильтрации. "
                f"Если вы запускаете только delete-тест — убедитесь, что товар уже создан."
            )

        row_locator = (
            By.XPATH,
            f"//form[@id='form-product']//tbody//tr[.//td//a[contains(normalize-space(), '{product_name}')] "
            f"or .//td[contains(normalize-space(), '{product_name}')]]",
        )
        rows = self.driver.find_elements(*row_locator)
        if not rows:
            names = self.driver.find_elements(
                By.CSS_SELECTOR, "#form-product tbody td.text-start"
            )
            preview = [n.text.strip() for n in names if n.text.strip()][:10]
            raise AssertionError(
                f"Не нашли строку товара '{product_name}' после фильтрации. "
                f"Примеры строк в таблице: {preview}"
            )

        row_el = rows[0]
        checkbox = row_el.find_element(
            By.CSS_SELECTOR, "input[name='selected[]'][type='checkbox']"
        )
        if not checkbox.is_selected():
            checkbox.click()

        delete_btn_el = self.wait_visible(
            self.DELETE_BTN, name="Кнопка Delete", timeout=10
        )
        self.scroll_into_view(delete_btn_el)
        self.js_click(delete_btn_el)

        self.accept_alert(timeout=5)

        success_alert = self.wait_visible(
            self.SUCCESS_DELETE, name="Алерт успеха удаления", timeout=10
        )
        assert ("Success" in success_alert.text) or (
            "modified" in success_alert.text
        ), f"Не нашли сообщение об успехе удаления. Текст алерта: {success_alert.text}"

        still_there = self.driver.find_elements(*row_locator)
        assert len(still_there) == 0, (
            "Товар всё еще отображается в списке после удаления!"
        )
        return self
