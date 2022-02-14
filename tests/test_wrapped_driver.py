"""test_wrapped_driver.py

Sort of Unit test for WrappedDriver class
"""
import pytest
from selenium.common.exceptions import WebDriverException

from wrappeddriver.wrappeddriver import WrappedDriver


def test_empty_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    with pytest.raises(WebDriverException):
        WrappedDriver(executable_path="", headless=True)


def test_no_chromedriver_path():
    """Assert error is raised if no chromedriver path is used"""
    # Disable all the no-value-for-parameter violations in this function
    # pylint: disable=no-value-for-parameter
    with pytest.raises(TypeError):
        WrappedDriver(headless=True)


def test_driver_set_window_size(bin_path):
    """Assert something after driver.close()"""
    expected_width = "800"
    expected_height = "800"
    with WrappedDriver(
        executable_path=f"{bin_path}/chromedriver",
        headless=True,
        window_size=(expected_width, expected_height),
    ) as driver:
        driver.open(url="https://www.google.com/")
        option_args_width, option_args_height = [
            x.split("=")[1] for x in driver.options.arguments if "window-size" in x
        ][0].split(",")

    assert option_args_width == expected_width, (
        f"Expected width {expected_width} did not match width {option_args_width} from "
        "driver.options.arguments"
    )
    assert option_args_height == expected_height, (
        f"Expected height {expected_height} did not match height {option_args_height} "
        "from driver.options.arguments"
    )
