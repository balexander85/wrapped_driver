import pytest

from wrapped_driver import WrappedDriver


CHROME_DRIVER_PATH = "/usr/bin/chromedriver"


class TestClass:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = WrappedDriver(
            chrome_driver_path=CHROME_DRIVER_PATH, headless=True,
        )
        self.driver.open("http://www.dadgumsalsa.com")

    def test_current_url(self):
        """Assert current_url property value"""
        assert self.driver.current_url == "http://dadgumsalsa.com/"

    def test_page_title(self):
        """Assert title property value"""
        assert self.driver.title == "DGS | Home"

