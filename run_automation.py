import time
import json
import os
from datetime import datetime
from tests.conftest import get_driver, logger
from pages.main_page import MainPage
from pages.login_page import LoginPage
from tests.test_01_login_ui import check_login_ui_case
from tests.test_02_login_func import check_login_func_case
import requests

# ---------------------------
# config.json 불러오기
# ---------------------------
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "config.json")
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

DOMAIN = cfg["testrail_domain"]
EMAIL = cfg["testrail_email"]
API_KEY = cfg["testrail_api_key"]
PROJECT_ID = cfg["project_id"]
SUITE_ID = cfg["suite_id"]

# ---------------------------
# TestRail Client
# ---------------------------
class TestRailClient:
    def __init__(self, domain, email, api_key, project_id, suite_id):
        self.url = domain
        self.email = email
        self.api_key = api_key
        self.project_id = project_id
        self.suite_id = suite_id
        self.auth = (self.email, self.api_key)

    def get_cases_in_suite(self, suite_id):
        endpoint = f"{self.url}/index.php?/api/v2/get_cases/{self.project_id}"
        params = {"suite_id": suite_id}
        try:
            resp = requests.get(endpoint, auth=self.auth, params=params)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"❌ TestRail 케이스 조회 실패: {e}")
            return []
        data = resp.json()
        cases = data.get("cases", [])
        return [c["id"] for c in cases]

    def create_test_run(self, name, include_all=True, case_ids=None):
        endpoint = f"{self.url}/index.php?/api/v2/add_run/{self.project_id}"
        payload = {
            "suite_id": self.suite_id,
            "name": name,
            "include_all": include_all,
        }
        if case_ids:
            payload["case_ids"] = case_ids
        try:
            resp = requests.post(endpoint, auth=self.auth, json=payload)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"❌ TestRail 테스트런 생성 실패: {e}")
            return None
        return resp.json()["id"]

    def add_result_for_case(self, run_id, case_id, status_id, comment=""):
        endpoint = f"{self.url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        payload = {"status_id": status_id, "comment": comment}
        try:
            resp = requests.post(endpoint, auth=self.auth, json=payload)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"❌ TestRail 결과 업로드 실패: {e}")
        return resp.json()


# ---------------------------
# TestRail Client 생성
# ---------------------------
testrail = TestRailClient(DOMAIN, EMAIL, API_KEY, PROJECT_ID, SUITE_ID)

# ---------------------------
# 테스트 케이스 조회
# ---------------------------
case_ids = testrail.get_cases_in_suite(SUITE_ID)
if not case_ids:
    logger.error("❌ 실행할 테스트케이스가 없습니다.")
    exit()

# ---------------------------
# 테스트런 이름 자동 생성 (현재 시간 기준)
# ---------------------------
run_name = f"자동화 테스트 - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
run_id = testrail.create_test_run(run_name, include_all=False, case_ids=case_ids)
if not run_id:
    logger.error("❌ 테스트런 생성 실패, 종료")
    exit()

logger.info(f"🟢 테스트런 생성 완료: Run ID {run_id}, 이름: {run_name}")

# ---------------------------
# 케이스 실행 루프
# ---------------------------
for case_id in case_ids:
    logger.info(f"🟡 케이스 실행 시작: Case ID {case_id}")

    driver = get_driver()
    main = MainPage(driver)
    login = LoginPage(driver)

    status_id = 1
    comment = ""

    try:
        if case_id in range(1, 9):
            # UI 테스트
            check_login_ui_case(driver, main, case_id)
            comment = "자동화 테스트 PASS"
        elif case_id in range(12, 15):
            # 기능 테스트
            check_login_func_case(driver, main, login, case_id)
            comment = "자동화 테스트 PASS"
        else:
            raise Exception(f"case_id {case_id} 미구현")

        logger.info(f"✅  케이스 PASS: {case_id}")

    except AssertionError as e:
        logger.error(f"❌ 케이스 FAIL: {case_id} - {e}")
        status_id = 5
        comment = str(e)

    except Exception as e:
        logger.warning(f"⚠️ 케이스 {case_id} 미구현 또는 예외 발생: {e}")
        status_id = 5
        comment = str(e)

    finally:
        driver.quit()

    testrail.add_result_for_case(run_id, case_id, status_id, comment)
    time.sleep(1)

logger.info("🟢 모든 테스트케이스 실행 완료")
