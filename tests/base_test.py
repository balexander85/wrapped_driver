import pytest

from wrapped_driver import WrappedDriver


TEST_SITE_URL = "http://www.dadgumsalsa.com"
TEST_SITE_TITLE = "DGS | Home"


class BaseTest:
    """Test class for basic webdriver methods"""

    driver: WrappedDriver

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.driver.open(TEST_SITE_URL)

    def test_current_url(self):
        """Assert current_url property value"""
        assert self.driver.current_url == TEST_SITE_URL

    def test_page_title(self):
        """Assert title property value"""
        assert self.driver.title == TEST_SITE_TITLE

    def test_driver_close(self):
        """Assert something after driver.close()"""
        self.driver.close()
        assert True
