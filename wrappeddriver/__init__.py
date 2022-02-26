"""__init__.py

Module for all webdriver classes and methods

Hopefully this works to allow for easier install as a dependency
"""
# from importlib import metadata
import logging
from sys import stdout
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from wrappeddriver.constants import (
    DEFAULT_DESKTOP_USER_AGENT,
    DEFAULT_DESKTOP_WINDOW_SIZE,
    LOGGER_FORMAT,
    MOBILE_USER_AGENT,
    get_chrome_options,
    get_firefox_options,
)


__title__ = __name__
# if you're stuck on python 3.7 or older, importlib-metadata is a
# third-party package that can be used as a drop-in instead
# __version__ = metadata.version(__title__)


logging.basicConfig(
    level=logging.INFO,
    format=LOGGER_FORMAT,
    stream=stdout,
)
LOGGER = logging.getLogger(__name__)


class WrappedDriver:
    """Class used to wrap selenium webdriver"""

    def __init__(
        self,
        executable_path: str,
        browser: str = "chrome",
        headless: bool = False,
        mobile: bool = False,
        **kwargs,
    ):
        if kwargs.get("user_agent"):
            user_agent = kwargs.get("user_agent")
        else:
            user_agent = DEFAULT_DESKTOP_USER_AGENT

        self.options = (
            get_firefox_options() if browser == "firefox" else get_chrome_options()
        )
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--no-sandbox")

        if kwargs.get("window_size"):
            width, height = kwargs.get("window_size")
            self.options.add_argument(f"--window-size={width},{height}")

        if mobile:
            self.options.add_argument(MOBILE_USER_AGENT)
        else:
            self.options.add_argument(user_agent)
            if not kwargs.get("window_size"):
                self.options.add_argument(
                    f"--window-size={DEFAULT_DESKTOP_WINDOW_SIZE}"
                )

        service = Service(executable_path=executable_path)
        if browser == "chrome":
            self.driver = webdriver.Chrome(service=service, options=self.options)
        elif browser == "firefox":
            self.driver = webdriver.Firefox(service=service, options=self.options)
        else:
            LOGGER.error("Invalid value for browser: %s", browser)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit_driver()

    def close(self):
        """Closes the current window."""
        LOGGER.debug("Closing window.")
        self.driver.close()

    @property
    def current_url(self) -> str:
        """Return the URL that the webdriver is at currently"""
        return self.driver.current_url

    def element_visible(self, locator: str = None, element: WebElement = None) -> bool:
        """Return bool for element visibility"""
        if not element:
            element = self.get_element_by_css(locator)
        return element.is_displayed()

    def element_exist(self, locator: str = None, element: WebElement = None) -> bool:
        """Return bool for element visibility"""
        try:
            if not element:
                element = self.get_element_by_css(locator)
            return element.is_displayed()
        except NoSuchElementException as error:
            LOGGER.debug(error)
        return False

    def delete_element(self, locator: str = None, element: WebElement = None):
        """Delete element with js .remove method"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        self.driver.execute_script("arguments[0].remove();", element)

    def get_console_logs(self) -> List[dict]:
        """Get console logs from the browser, I think this only available in Chrome"""
        return self.driver.get_log("browser")

    def get_element_by_id(self, element_id: str) -> WebElement:
        """Find element by element ID and return element"""
        return self.driver.find_element(by=By.ID, value=element_id)

    def get_element_by_css(self, locator: str) -> WebElement:
        """Find element by css locator and return element"""
        return self.driver.find_element(by=By.CSS_SELECTOR, value=locator)

    def get_elements_by_css(self, locator: str) -> List[WebElement]:
        """Find elements by css locator and return element"""
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=locator)

    def get_element_by_text(self, text: str) -> WebElement:
        """Find element by element text and return element"""
        return self.driver.find_element(by=By.XPATH, value=f"//*[text()='{text}']")

    def highlight_element(
        self, locator: str = None, element: WebElement = None, color: str = "red"
    ):
        """Highlight element by adding color to borders of element"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        self.driver.execute_script(
            f"arguments[0].style.border='3px solid {color}'", element
        )

    def maximize_window(self):
        """Maximize window"""
        self.driver.maximize_window()

    def move_mouse_by_offset(self, x_offset, y_offset):
        """Helper method to move cursor off screen"""
        LOGGER.debug("Moving cursor off screen")
        ActionChains(self.driver).move_by_offset(
            xoffset=x_offset, yoffset=y_offset
        ).perform()

    def open(self, url: str):
        """Open page for URL passed in"""
        LOGGER.debug("self.open(): self.driver.get(%s)", url)
        self.driver.get(url)

    def quit_driver(self):
        """Closes the browser and shuts down the ChromeDriver executable."""
        LOGGER.debug("Closing browser and shutting down ChromeDriver instance")
        self.driver.quit()

    def refresh(self):
        """Refresh page with driver.refresh()"""
        self.driver.refresh()

    def screenshot_element(
        self, locator: str = None, element: WebElement = None, file_name: str = ""
    ):
        """Screenshot element with element.screenshot()"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        element.screenshot(filename=file_name)

    def scroll_to_element(self, locator: str = None, element: WebElement = None):
        """Helper method to scroll down to element"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        LOGGER.debug("Scrolling to WebElement: %s", element)
        ActionChains(self.driver).move_to_element(element).perform()

    @property
    def switch_to(self):
        """Wrapped method of selenium webdriver switch_to"""
        return self.driver.switch_to

    @property
    def title(self) -> str:
        """Return page title <title>"""
        return self.driver.title
