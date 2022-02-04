from platform import platform

import pytest

from wrappeddriver import WrappedDriver


if "macOS" in platform():
    CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
    GECKODRIVER_PATH = "/opt/homebrew/bin/geckodriver"
else:
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
    GECKODRIVER_PATH = "/usr/bin/geckodriver"


@pytest.fixture(autouse=True, name="driver")
def wrapped_driver(request) -> WrappedDriver:
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
