from pages.base_method import BaseMethod
from data.json_loader import load_json

class HeaderPage(BaseMethod):
    def __init__(self, driver):
        locators = load_json("header_data.json")
        func_locators = load_json("login_func_data.json")
        locators.update(func_locators)
        super().__init__(driver, locators=locators)

    # GNB 메뉴 클릭
    def click_menu(self):
        return self.click_element("menu_button")

    # 로그인 메뉴 클릭
    def click_login_item(self):
        return self.click_element("login_menu_item")

    # 로그아웃 메뉴 화면 노출 확인
    def is_logout_visible(self):
        return self.is_element_visible("logout_menu_item")
