from pages.login_page import go_to_login_page
from tests.conftest import logger

def check_login_ui_case(driver, main, case_id):
    # ✅ 사전 조건: 로그인 페이지 진입
    go_to_login_page(driver, main)

    if case_id == 1:
        logger.info("🟡 케이스 1: 헤더 노출 확인 🟡")
        assert main.is_element_visible("header"), "로그인 페이지 헤더가 화면에 나타나지 않음"
    elif case_id == 2:
        logger.info("🟡 케이스 2: login_page_title 노출 확인 🟡")
        assert main.is_element_visible("login_page_title"), "login_page_title 요소가 화면에 나타나지 않음"
    elif case_id == 3:
        logger.info("🟡 케이스 3: login_guide_text 노출 확인 🟡")
        assert main.is_element_visible("login_guide_text"), "login_guide_text 요소가 화면에 나타나지 않음"
    elif case_id == 4:
        logger.info("🟡 케이스 4: username_label 노출 확인 🟡")
        assert main.is_element_visible("username_label"), "username_label 요소가 화면에 나타나지 않음"
    elif case_id == 5:
        logger.info("🟡 케이스 5: username_input 노출 확인 🟡")
        assert main.is_element_visible("username_input"), "username_input 요소가 화면에 나타나지 않음"
    elif case_id == 6:
        logger.info("🟡 케이스 6: password_label 노출 확인 🟡")
        assert main.is_element_visible("password_label"), "password_label 요소가 화면에 나타나지 않음"
    elif case_id == 7:
        logger.info("🟡 케이스 7: password_input 노출 확인 🟡")
        assert main.is_element_visible("password_input"), "password_input 요소가 화면에 나타나지 않음"
    elif case_id == 8:
        logger.info("🟡 케이스 8: login_button 노출 확인 🟡")
        assert main.is_element_visible("login_button"), "login_button 요소가 화면에 나타나지 않음"
    else:
        logger.warning(f"⚠️ 정의되지 않은 케이스 ID: {case_id}")

    logger.info(f"✅  케이스 {case_id} UI 확인 완료")