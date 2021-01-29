import pytest
from selenium.common.exceptions import WebDriverException

from wrapped_driver import WrappedDriver


def test_empty_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(WebDriverException):
        WrappedDriver(chrome_driver_path="", headless=True)


def test_no_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(TypeError):
        WrappedDriver(headless=True)
