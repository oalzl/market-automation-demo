import pytest
from pages.login_page import go_to_login_page
from tests.conftest import logger

def check_login_func_case(driver, main, login, case_id):
    # ✅ 사전 조건: 로그인 페이지 진입
    go_to_login_page(driver, main)

    # valid credential 가져오기
    valid_username = login.locators["credentials"]["valid"]["username"]
    valid_password = login.locators["credentials"]["valid"]["password"]

    if case_id == 12:
        logger.info("🟡 케이스 12: 로그인 완료 확인 🟡")

        # Username / Password 필드 확인 및 입력
        assert login.is_element_visible("username_input"), "Username 입력 필드 노출 실패"
        login.input_text("username_input", valid_username)
        assert login.is_element_visible("password_input"), "Password 입력 필드 노출 실패"
        login.input_text("password_input", valid_password)

        login.click_login()
        logger.info("✅  로그인 버튼 클릭 완료")

        # 헤더 메뉴 버튼 나타날 때까지 기다렸다가 클릭
        assert main.header.is_element_visible("menu_button"), "헤더 메뉴 버튼 노출 실패"
        main.header.click_menu()

        # 로그아웃 메뉴 노출 확인
        assert main.header.is_logout_visible(), "로그인 완료 후 로그아웃 메뉴가 보이지 않음"

    elif case_id == 13:
        logger.info("🟡 케이스 13: Username 미입력 시 오류 확인 🟡")

        # Username 미입력 / Password는 valid 사용
        login.input_text("username_input", "")
        login.input_text("password_input", valid_password)
        login.click_login()

        # 오류 메시지 확인
        assert login.check_result("username_empty"), "Username 미입력 오류 메시지 확인 실패"

    elif case_id == 14:
        logger.info("🟡 케이스 14: Password 미입력 시 오류 확인 🟡")

        # Username은 valid 사용 / Password 미입력
        login.input_text("username_input", valid_username)
        login.input_text("password_input", "")
        login.click_login()

        # 오류 메시지 확인
        assert login.check_result("password_empty"), "Password 미입력 오류 메시지 확인 실패"

    else:
        logger.warning(f"⚠️ 정의되지 않은 케이스 ID: {case_id}")

    logger.info(f"✅  케이스 {case_id} 기능 테스트 완료")
