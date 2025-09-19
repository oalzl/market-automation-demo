import pytest
from pages.main_page import MainPage
from tests.conftest import logger

# -----------------------
# 로그인 페이지 UI 확인 함수
# -----------------------
def check_login_page_ui(main):
    logger.info("🟡 로그인 페이지 UI 확인 🟡")

    # 헤더 확인
    logger.info("➡️ 로그인 페이지 헤더 확인")
    assert main.is_element_visible("header"), "로그인 페이지 헤더가 화면에 나타나지 않음"
    logger.info("✅  로그인 페이지 헤더 확인 완료")

    # 기타 UI 요소 확인
    ui_elements = [
        "login_page_title",
        "login_guide_text",
        "username_label",
        "username_input",
        "password_label",
        "password_input",
        "login_button"
    ]

    for key in ui_elements:
        logger.info(f"➡️ '{key}' 노출 확인 시작")
        assert main.is_element_visible(key), f"{key} 요소가 화면에 나타나지 않음"
        logger.info(f"✅  '{key}' 노출 확인 완료")

    logger.info("🟢 로그인 페이지 UI 확인 완료 🟢")


# -----------------------
# 테스트 함수
# -----------------------
def test_login_page_ui(driver):
    main = MainPage(driver)

    logger.info("🟡 로그인 페이지 진입 시작 🟡")

    # GNB 메뉴 확인 후 클릭
    logger.info("➡️ GNB 메뉴가 화면에 나타날 때까지 대기")
    assert main.header.is_element_visible("menu_button"), "GNB 메뉴 버튼이 화면에 나타나지 않음"
    logger.info("✅  GNB 메뉴 확인 완료")

    logger.info("➡️ 로그인 메뉴 클릭")
    main.open_login_menu()
    logger.info("✅  로그인 페이지 진입 완료")

    # 로그인 페이지 UI 확인 함수 호출
    check_login_page_ui(main)
