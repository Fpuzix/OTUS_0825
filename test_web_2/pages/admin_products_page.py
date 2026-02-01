import time

from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminProductsPage(BasePage):
    MENU_CATALOG = (By.CSS_SELECTOR, "#menu-catalog > a")
    SUBMENU_PRODUCTS = (By.LINK_TEXT, "Products")

    ADD_NEW_BTN = (
        By.CSS_SELECTOR,
        "a[href*='catalog/product.form'], a[href*='catalog/product|add']",
    )
    NAME_FIELD = (By.ID, "input-name-1")
    META_FIELD = (By.ID, "input-meta-title-1")
    TAB_DATA = (By.LINK_TEXT, "Data")
    MODEL_FIELD = (By.ID, "input-model")
    TAB_SEO = (By.LINK_TEXT, "SEO")
    SEO_FIELD = (By.CSS_SELECTOR, "input[name='product_seo_url[0][1]']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[form='form-product']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success, .alert-dismissible")

    FILTER_NAME = (By.ID, "input-name")
    FILTER_BTN = (By.ID, "button-filter")
    DELETE_BTN = (
        By.CSS_SELECTOR,
        "button[data-oc-action*='product|delete'], .btn-danger",
    )
    SUCCESS_DELETE = (By.CSS_SELECTOR, ".alert-success")

    def open_products_list(self):
        catalog_menu = self.wait_visible(self.MENU_CATALOG, name="Меню Catalog")
        catalog_menu.click()

        products_link = self.wait_visible(
            self.SUBMENU_PRODUCTS, name="Подменю Products"
        )
        self.js_click(products_link)

    def add_new_product(
        self, name: str, meta_title: str, model: str, seo_prefix="test-product"
    ):
        add_new_btn = self.wait_visible(self.ADD_NEW_BTN, name="Кнопка Добавить новый")
        self.scroll_into_view(add_new_btn)
        self.js_click(add_new_btn)

        name_field = self.wait_visible(self.NAME_FIELD, name="Product Name")
        name_field.clear()
        name_field.send_keys(name)

        meta_field = self.wait_visible(self.META_FIELD, name="Meta Tag Title")
        meta_field.clear()
        meta_field.send_keys(meta_title)

        tab_data = self.wait_visible(self.TAB_DATA, name="Вкладка Data")
        self.js_click(tab_data)

        model_field = self.wait_visible(self.MODEL_FIELD, name="Model")
        model_field.clear()
        model_field.send_keys(model)

        tab_seo = self.wait_visible(self.TAB_SEO, name="Вкладка SEO")
        self.js_click(tab_seo)

        seo_field = self.wait_visible(self.SEO_FIELD, name="SEO Keyword Field")
        self.scroll_into_view(seo_field)
        seo_field.clear()
        seo_field.send_keys(f"{seo_prefix}-{int(time.time())}")

        save_button = self.wait_visible(self.SAVE_BUTTON, name="Кнопка Сохранить")
        self.scroll_into_view(save_button)
        self.js_click(save_button)

        success_alert = self.wait_visible(
            self.SUCCESS_ALERT, name="Алерт успеха", timeout=10
        )
        assert ("Success" in success_alert.text) or (
            "You have modified products" in success_alert.text
        )

    def delete_product_by_name(self, product_name: str):
        filter_name = self.wait_visible(self.FILTER_NAME, name="Фильтр по имени")
        filter_name.clear()
        filter_name.send_keys(product_name)

        self.driver.find_element(*self.FILTER_BTN).click()

        checkbox = self.wait_visible(
            (
                By.XPATH,
                f"//td[contains(text(), '{product_name}')]/preceding-sibling::td/input[@type='checkbox']",
            ),
            name="Чекбокс товара",
            timeout=10,
        )
        if not checkbox.is_selected():
            checkbox.click()

        delete_button = self.wait_visible(self.DELETE_BTN, name="Кнопка Удалить")
        delete_button.click()

        self.accept_alert(timeout=5)

        success_alert = self.wait_visible(
            self.SUCCESS_DELETE, name="Алерт успеха удаления"
        )
        assert ("Success" in success_alert.text) or ("modified" in success_alert.text)

        no_results = self.driver.find_elements(
            By.XPATH, f"//td[contains(text(), '{product_name}')]"
        )
        assert len(no_results) == 0, (
            "Товар всё еще отображается в списке после удаления!"
        )
