import pytest
from config.config import get_driver

@pytest.fixture(scope="module")
def driver():
    drv = get_driver()
    yield drv
    drv.quit()

def test_open_app(driver):

    pass
