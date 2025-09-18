from appium import webdriver
from appium.options.android import UiAutomator2Options

CONFIG = {
    "platform_name": "Android",
    "platform_version": "16",
    "device_name": "emulator-5554",
    "app_package": "com.saucelabs.mydemoapp.android",
    "app_activity": ".view.activities.SplashActivity",
    "appium_server": "http://127.0.0.1:4723",
}

def get_driver():
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
    return driver
