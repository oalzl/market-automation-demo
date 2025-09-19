import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

class BaseMethod:
    def __init__(self, driver, locators=None, wait_time=10, retry_count=5):
        self.driver = driver
        self.locators = locators or {}
        self.wait = WebDriverWait(driver, wait_time)
        self.retry_count = retry_count
        self.logger = logging.getLogger(__name__)

    # -----------------------
    # 재시도 공통 함수
    # -----------------------
    def _retry_action(self, action_func, action_desc):
        for attempt in range(1, self.retry_count + 1):
            try:
                return action_func()
            except (StaleElementReferenceException, TimeoutException) as e:
                self.logger.warning(f"{action_desc} 실패 시도 {attempt}/{self.retry_count}: {e}")
                time.sleep(0.5)
        raise Exception(f"{action_desc}를 {self.retry_count}회 시도했으나 실패했습니다.")

    # -----------------------
    # 요소 가시성 확인
    # -----------------------
    def is_element_visible(self, key: str) -> bool:
        xpath = self.locators.get(key)
        if not xpath:
            raise ValueError(f"{key} locator가 없습니다.")
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    def is_element_visible_by_xpath(self, xpath: str) -> bool:
        """직접 xpath를 사용하여 화면 노출 여부 확인"""
        if not xpath:
            raise ValueError("xpath가 비어있습니다.")
        try:
            return self.driver.find_element("xpath", xpath).is_displayed()
        except NoSuchElementException:
            return False

    # -----------------------
    # 클릭 / 입력
    # -----------------------
    def click_element(self, key: str) -> bool:
        xpath = self.locators.get(key)
        if not xpath:
            raise ValueError(f"{key} locator가 없습니다.")

        def action():
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
            time.sleep(0.5)  # 클릭 후 화면 전환 반영
            return True  # run_steps에서 assert용

        return self._retry_action(action, f"'{key}' 클릭")

    def input_text(self, key: str, text: str) -> bool:
        xpath = self.locators.get(key)
        if not xpath:
            raise ValueError(f"{key} locator가 없습니다.")

        def action():
            element = self.driver.find_element(By.XPATH, xpath)
            element.clear()
            element.send_keys(text)
            return True

        return self._retry_action(action, f"'{key}' 입력")

    # -----------------------
    # 검증 / 일치 확인
    # -----------------------
    def get_element_text(self, key: str) -> str:
        """locator key에 해당하는 요소의 텍스트를 반환"""
        xpath = self.locators.get(key)
        if not xpath:
            raise ValueError(f"{key} locator가 없습니다.")
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element.text
        except NoSuchElementException:
            raise Exception(f"{key} 요소를 찾을 수 없습니다.")

    def assert_saved_text_equals(self, key: str):
        if self.saved_text is None:
            raise Exception("저장된 텍스트가 없습니다.")
        current_text = self.get_element_text(key)
        self.logger.info(f"💡 저장된 텍스트: '{self.saved_text}'")
        self.logger.info(f"💡 현재 요소 텍스트: '{current_text}'")
        assert self.saved_text == current_text, f"상품명 불일치: {self.saved_text} != {current_text}"
        return True

    # -----------------------
    # 스크롤 / 스와이프 관련
    # -----------------------
    def _swipe(self, direction):
        """좌/우 스와이프 (Appium 전용)"""
        size = self.driver.get_window_size()
        start_y = size['height'] * 0.1
        start_x = size['width'] * 0.8
        end_x = size['width'] * 0.2

        if direction == "left":
            self.driver.swipe(start_x, start_y, end_x, start_y, 500)
        elif direction == "right":
            self.driver.swipe(end_x, start_y, start_x, start_y, 500)
        elif direction == "up":
            self.driver.swipe(start_x, size['height']*0.8, start_x, size['height']*0.2, 500)
        elif direction == "down":
            self.driver.swipe(start_x, size['height']*0.2, start_x, size['height']*0.8, 500)

    def scroll_element_to_center(self, key: str, max_swipes=15, tolerance=0.07):
        """
        요소가 화면 중앙 근처에 오도록 반복 스크롤
        :param key: locators에서 정의된 요소 key
        :param max_swipes: 최대 스와이프 횟수
        :param tolerance: 중앙 허용 범위 비율 (0~0.5), 화면 높이 기준
        """
        xpath = self.locators.get(key)
        if not xpath:
            raise ValueError(f"{key} locator가 없습니다.")

        window_size = self.driver.get_window_size()
        window_height = window_size['height']
        window_center_y = window_height / 2
        start_x = window_size['width'] / 2
        tolerance_px = window_height * tolerance

        for attempt in range(max_swipes):
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                element_center_y = element.location['y'] + element.size['height'] / 2
                offset = element_center_y - window_center_y

                # 요소가 허용 범위 안에 들어오면 종료
                if abs(offset) <= tolerance_px:
                    return True

                # 스와이프 거리: offset 절반 + 최소 스와이프 10% 화면 높이
                swipe_distance = max(abs(offset) / 2, window_height * 0.1)

                if offset > 0:
                    # 요소가 중앙보다 아래 → 위로 스와이프
                    self.driver.swipe(start_x, window_center_y, start_x, window_center_y - swipe_distance, 400)
                else:
                    # 요소가 중앙보다 위 → 아래로 스와이프
                    self.driver.swipe(start_x, window_center_y, start_x, window_center_y + swipe_distance, 400)

                time.sleep(0.3)

            except NoSuchElementException:
                time.sleep(0.3)

        raise Exception(f"{key} 요소를 화면 중앙 근처로 스크롤하지 못했습니다.")

    def scroll_until_xpath_visible(
            self,
            locator: str,
            direction: str = "up",
            max_swipes: int = 15,
            swipe_ratio: float = 0.5,
            tolerance: float = 0.07
    ):
        """
        locator가 가리키는 요소가 화면에 보일 때까지 스크롤하고,
        보이면 scroll_element_to_center() 호출하여 화면 중앙으로 이동
        """
        xpath = self.locators.get(locator, locator)
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] / 2

        for attempt in range(max_swipes):
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                if element.is_displayed():
                    # 여기서 scroll_element_to_center 호출
                    self.scroll_element_to_center(locator, max_swipes=5, tolerance=tolerance)
                    return True
            except NoSuchElementException:
                pass

            # 요소가 안 보이면 지정 방향으로 스와이프
            swipe_distance = window_size['height'] * swipe_ratio
            if direction == "up":
                self.driver.swipe(start_x, start_y, start_x, start_y - swipe_distance, 500)
            elif direction == "down":
                self.driver.swipe(start_x, start_y, start_x, start_y + swipe_distance, 500)
            elif direction == "left":
                end_x = start_x - window_size['width'] * swipe_ratio
                self.driver.swipe(start_x, start_y, end_x, start_y, 500)
            elif direction == "right":
                end_x = start_x + window_size['width'] * swipe_ratio
                self.driver.swipe(start_x, start_y, end_x, start_y, 500)

            time.sleep(0.3)

        raise Exception(f"{xpath} 요소를 {max_swipes}번 스와이프했지만 찾지 못했습니다.")
