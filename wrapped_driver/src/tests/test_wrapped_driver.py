import pytest
from selenium.common.exceptions import WebDriverException

from wrapped_driver import WrappedDriver


CHROME_DRIVER_PATH = "/usr/bin/chromedriver"


def test_basic_wrapped_driver():
    """Open driver and navigate to web page"""
    with WrappedDriver(chrome_driver_path=CHROME_DRIVER_PATH, headless=True,) as driver:
        driver.open("http://www.dadgumsalsa.com")


def test_page_title():
    """Open driver and navigate to web page"""
    with WrappedDriver(chrome_driver_path=CHROME_DRIVER_PATH, headless=True,) as driver:
        driver.open("http://www.dadgumsalsa.com")
        page_title = driver.title
    assert page_title == "DGS | Home"


def test_empty_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(WebDriverException):
        WrappedDriver(chrome_driver_path="", headless=True)


def test_no_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(TypeError):
        WrappedDriver(headless=True)

