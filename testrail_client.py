import requests
from tests.conftest import logger

class TestRailClient:
    def __init__(self, domain, email, api_key, project_id, suite_id):
        self.url = domain
        self.email = email
        self.api_key = api_key
        self.project_id = project_id
        self.suite_id = suite_id
        self.auth = (self.email, self.api_key)

    # 섹션 상관없이 Suite 내 전체 케이스 조회
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

    # TestRun 생성
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

    # 결과 업로드
    def add_result_for_case(self, run_id, case_id, status_id, comment=""):
        endpoint = f"{self.url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        payload = {"status_id": status_id, "comment": comment}
        try:
            resp = requests.post(endpoint, auth=self.auth, json=payload)
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"❌ TestRail 결과 업로드 실패: {e}")
        return resp.json()
