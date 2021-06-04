import pytest

from wrapped_driver import WrappedDriver


class BaseTest:
    """Test class for basic webdriver methods"""

    driver: WrappedDriver

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.driver.open("http://www.dadgumsalsa.com")

    def test_current_url(self):
        """Assert current_url property value"""
        assert self.driver.current_url == "http://dadgumsalsa.com/"

    def test_page_title(self):
        """Assert title property value"""
        assert self.driver.title == "DGS | Home"

    def test_driver_close(self):
        """Assert something after driver.close()"""
        self.driver.close()
        assert True
