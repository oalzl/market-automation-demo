import logging
import sys
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import CONFIG
import os

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
# Appium driver fixture
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

    driver = webdriver.Remote(
        command_executor=CONFIG["appium_server"],
        options=options
    )
    yield driver
    driver.quit()