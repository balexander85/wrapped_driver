"""conftest.py

File for test fixtures
"""
from platform import platform

import pytest

from wrappeddriver import WrappedDriver


if "macOS" in platform():
    CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
    GECKODRIVER_PATH = "/opt/homebrew/bin/geckodriver"
else:
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
    GECKODRIVER_PATH = "/usr/bin/geckodriver"


@pytest.fixture(autouse=True, name="bin_path")
def get_bin_path() -> str:
    """Return bin path based on OS

    Note:
        * Trying to develop on mac but actually run on raspberry pi
    """
    if "macOS" in platform():
        return "/opt/homebrew/bin"
    return "/usr/bin"


@pytest.fixture(autouse=True, name="driver")
def wrapped_driver(request) -> WrappedDriver:
    """Fixture to return instance of WrappedDriver"""
    browser_name = "firefox" if "FireFox" in str(request.cls) else "chrome"
    executable_path = (
        GECKODRIVER_PATH if "firefox" == browser_name else CHROME_DRIVER_PATH
    )
    with WrappedDriver(
        executable_path=executable_path,
        browser=browser_name,
        headless=True,
    ) as driver:
        yield driver
