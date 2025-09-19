from pages.base_method import BaseMethod
from data.json_loader import load_json

class LoginPage(BaseMethod):
    def __init__(self, driver):
        locators_ui = load_json("login_ui_data.json")
        locators_func = load_json("login_func_data.json")
        locators_ui.update(locators_func)  # UI + 기능 합치기
        super().__init__(driver, locators=locators_ui)

    def input_username(self, username):
        self.input_text("username_input", username)

    def input_password(self, password):
        self.input_text("password_input", password)

    def click_login(self):
        self.click_element("login_button")

    def check_result(self, key):
        """
        key: 'logout_menu_item', 'username_empty', 'password_empty'
        """
        val = self.locators.get(key)
        if isinstance(val, dict):
            # text + icon 확인
            return self.is_element_visible_by_xpath(val.get("text")) and \
                   self.is_element_visible_by_xpath(val.get("icon"))
        return self.is_element_visible_by_xpath(val)
