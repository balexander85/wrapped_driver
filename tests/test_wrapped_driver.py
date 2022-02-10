"""test_wrapped_driver.py

Sort of Unit test for WrappedDriver class
"""
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


def test_driver_set_window_size(bin_path):
    """Assert something after driver.close()"""
    with WrappedDriver(executable_path=f"{bin_path}/chromedriver", headless=True,
                       window_size=(800, 800)) as driver:
        driver.open(url="https://www.google.com/")

    assert True
