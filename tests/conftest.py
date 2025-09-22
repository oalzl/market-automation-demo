import logging
import sys
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import CONFIG
from pages.main_page import MainPage
from pages.login_page import LoginPage, go_to_login_page

# -----------------------
# 로거 설정
# -----------------------
logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# -----------------------
# Appium driver fixture (pytest용)
# -----------------------
@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = CONFIG["platform_name"]
    options.platform_version = CONFIG["platform_version"]
    options.device_name = CONFIG["device_name"]
    options.app_package = CONFIG["app_package"]
    options.app_activity = CONFIG["app_activity"]
    options.auto_grant_permissions = True

    drv = webdriver.Remote(
        command_executor=CONFIG["appium_server"],
        options=options
    )
    yield drv
    drv.quit()

# -----------------------
# 독립 실행용 get_driver() 함수
# -----------------------
def get_driver():
    options = UiAutomator2Options()
    options.platform_name = CONFIG["platform_name"]
    options.platform_version = CONFIG["platform_version"]
    options.device_name = CONFIG["device_name"]
    options.app_package = CONFIG["app_package"]
    options.app_activity = CONFIG["app_activity"]
    options.auto_grant_permissions = True

    drv = webdriver.Remote(
        command_executor=CONFIG["appium_server"],
        options=options
    )
    return drv


@pytest.fixture
def login_page(driver):
    """
    로그인 페이지 진입 후 MainPage, LoginPage 반환
    """
    main = MainPage(driver)
    go_to_login_page(driver, main)
    login = LoginPage(driver)
    return main, login
