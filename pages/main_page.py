from pages.base_method import BaseMethod
from pages.header_page import HeaderPage
from data.json_loader import load_json

class MainPage(BaseMethod):
    def __init__(self, driver):
        locators = load_json("login_ui_data.json")
        super().__init__(driver, locators=locators)
        self.header = HeaderPage(driver)

    def open_login_menu(self):
        self.header.click_menu()
        self.header.click_login_item()
