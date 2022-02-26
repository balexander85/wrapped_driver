"""constants.py

Collection of constants used in wrappeddriver.py
"""
from selenium import webdriver


DEFAULT_DESKTOP_USER_AGENT = (
    "user-agent=Mozilla/5.0 "
    "(Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
)
DEFAULT_DESKTOP_WINDOW_SIZE = "1920,1080"
LOGGER_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
MOBILE_USER_AGENT = (
    "user-agent=Mozilla/5.0 "
    "(iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/13.0.3 Mobile/15E148 Safari/604.1"
)


def get_chrome_options() -> webdriver.ChromeOptions:
    """Return ChromeOptions object for chromedriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    return chrome_options


def get_firefox_options() -> webdriver.FirefoxOptions:
    """Return FirefoxOptions object for geckodriver"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--disable-features=VizDisplayCompositor")
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--disable-gpu")
    return firefox_options
