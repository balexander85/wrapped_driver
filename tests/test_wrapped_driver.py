from wrapped_driver import WrappedDriver


CHROME_DRIVER_PATH = ""


def test_basic_wrapped_driver():
    """Open driver and navigate to web page"""
    with WrappedDriver(chrome_driver_path=CHROME_DRIVER_PATH, headless=True,) as driver:
        driver.open("http://www.google.com")
