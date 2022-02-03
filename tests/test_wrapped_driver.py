import pytest
from selenium.common.exceptions import WebDriverException

from wrappeddriver import WrappedDriver


def test_empty_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(WebDriverException):
        WrappedDriver(executable_path="", headless=True)


def test_no_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(TypeError):
        WrappedDriver(headless=True)
