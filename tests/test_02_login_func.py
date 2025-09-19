import time
import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from tests.conftest import logger
from data.json_loader import load_json

func_data = load_json("login_func_data.json")

# -----------------------
# 로그인 기능 테스트
# -----------------------
@pytest.mark.parametrize(
    "username,password,expected_key,desc",
    [
        (
            func_data["credentials"]["valid"]["username"],
            func_data["credentials"]["valid"]["password"],
            "logout_menu_item",
            "로그인 성공",
        ),
        (
            "",
            func_data["credentials"]["valid"]["password"],
            "username_empty",
            "username 미입력",
        ),
        (
            func_data["credentials"]["valid"]["username"],
            "",
            "password_empty",
            "password 미입력",
        ),
    ],
)
def test_login_function(driver, username, password, expected_key, desc):
    logger.info(f"🟡 로그인 기능 테스트 시작 : {desc} 🟡")

    # -----------------------
    # 앱 메인 진입 + 로그인 메뉴
    # -----------------------
    logger.info("➡️ GNB 메뉴 확인 시작")
    main = MainPage(driver)
    assert main.header.is_element_visible("menu_button"), "GNB 메뉴 버튼이 화면에 나타나지 않음"
    logger.info("✅  GNB 메뉴 확인 완료")

    logger.info("➡️ 로그인 메뉴 클릭 시작")
    main.open_login_menu()
    logger.info("✅  로그인 메뉴 클릭 완료")

    # -----------------------
    # LoginPage에서 입력/클릭
    # -----------------------
    login = LoginPage(driver)

    if username:
        logger.info("➡️ Username 입력 시작")
        login.input_text("username_input", username)
        logger.info("✅  Username 입력 완료")

    if password:
        logger.info("➡️ Password 입력 시작")
        login.input_text("password_input", password)
        logger.info("✅  Password 입력 완료")

    logger.info("➡️ 로그인 버튼 클릭 시작")
    login.click_login()
    time.sleep(1)  # 로그인 처리 대기
    logger.info("✅  로그인 버튼 클릭 완료")

    # -----------------------
    # 결과 확인
    # -----------------------
    logger.info(f"➡️ '{desc}' 결과 확인 시작")
    if desc == "로그인 성공":
        logger.info("➡️ GNB 메뉴 열기 시작 (로그인 성공 확인용)")
        main.header.click_menu()
        logger.info("✅  GNB 메뉴 열기 완료")

        logger.info("➡️ 로그아웃 메뉴 확인 시작")
        assert main.header.is_logout_visible(), f"{desc} 검증 실패"
        logger.info("✅  로그아웃 메뉴 확인 완료")
    else:
        logger.info("➡️ 오류 메시지 확인 시작")
        assert login.check_result(expected_key), f"{desc} 검증 실패"
        logger.info("✅  오류 메시지 확인 완료")

    logger.info(f"🟡 로그인 기능 테스트 확인 완료 : {desc} 🟡")
