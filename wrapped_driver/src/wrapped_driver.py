"""wrapped_driver.py

Module for all webdriver classes and methods
"""
import logging
from sys import stdout
from typing import List

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    stream=stdout,
)
LOGGER = logging.getLogger(__name__)


USER_AGENT = (
    "user-agent=Mozilla/5.0 "
    "(Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
)

MOBILE_USER_AGENT = (
    "user-agent=Mozilla/5.0 "
    "(iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/13.0.3 Mobile/15E148 Safari/604.1"
)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")


class WrappedDriver:
    """Class used to wrap selenium webdriver"""

    def __init__(
        self,
        chrome_driver_path: str,
        browser: str = "chrome",
        headless: bool = False,
        user_agent: str = USER_AGENT,
    ):
        if headless:
            chrome_options.add_argument("--headless")
            # needed for docker
            chrome_options.add_argument("--no-sandbox")

        if browser == "chrome":
            chrome_options.add_argument(user_agent)
            chrome_options.add_argument("--window-size=1920,1080")
            self.driver = webdriver.Chrome(
                executable_path=chrome_driver_path, options=chrome_options
            )
        elif browser == "mobile":
            chrome_options.add_argument(MOBILE_USER_AGENT)
            self.driver = webdriver.Chrome(
                executable_path=chrome_driver_path, options=chrome_options
            )
        else:
            LOGGER.error(f"Invalid value for browser: {browser}")

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
        return self.driver.current_url

    def element_visible(self, locator: str = None, element: WebElement = None) -> bool:
        """Return bool for element visibility"""
        if not element:
            element = self.get_element_by_css(locator)
        return element.is_displayed()

    def delete_element(self, locator: str = None, element: WebElement = None):
        """Delete element with js .remove method"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        self.driver.execute_script("arguments[0].remove();", element)

    def get_element_by_id(self, element_id: str) -> WebElement:
        return self.driver.find_element_by_id(element_id)

    def get_elements_by_id(self, element_id: str) -> List[WebElement]:
        return self.driver.find_elements_by_id(element_id)

    def get_element_by_css(self, locator: str) -> WebElement:
        return self.driver.find_element_by_css_selector(css_selector=locator)

    def get_elements_by_css(self, locator: str) -> List[WebElement]:
        return self.driver.find_elements_by_css_selector(css_selector=locator)

    def highlight_element(
        self, locator: str = None, element: WebElement = None, color: str = "red"
    ):
        """Highlight element by adding color to borders of element"""
        if not element:
            element = self.get_element_by_css(locator=locator)
        self.driver.execute_script(
            f"arguments[0].style.border='3px solid {color}'", element
        )

    def move_mouse_by_offset(self, x, y):
        """Helper method to move cursor off screen"""
        LOGGER.debug(f"Moving cursor off screen")
        ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=y).perform()

    def open(self, url: str):
        LOGGER.debug(f"self.open(): self.driver.get({url})")
        self.driver.get(url)

    def quit_driver(self):
        """Closes the browser and shuts down the ChromeDriver executable."""
        LOGGER.debug("Closing browser and shutting down ChromeDriver instance")
        self.driver.quit()

    def scroll_to_element(self, element: WebElement):
        """Helper method to scroll down to element"""
        LOGGER.debug(f"Scrolling to WebElement: {element}")
        ActionChains(self.driver).move_to_element(element).perform()

    @property
    def switch_to(self):
        """Wrapped method of selenium webdriver switch_to"""
        return self.driver.switch_to

    @property
    def title(self) -> str:
        return self.driver.title

    def wait_for_element_to_be_present_by_id(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_present(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_visible_by_id(
            self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_visible(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_present_by_css(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_present(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_not_to_be_present_by_css(
        self, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_not_to_be_present(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_visible_by_css(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_visible(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_not_to_be_visible_by_css(
        self, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_not_to_be_visible(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_present(
        self, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present"""
        LOGGER.debug(msg=f"Waiting for locator to be present: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until(EC.presence_of_element_located((by, locator)))

    def wait_for_element_not_to_be_present(
        self, by: By, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present"""
        LOGGER.debug(msg=f"Waiting for locator to NOT be present: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until_not(EC.presence_of_element_located((by, locator)))

    def wait_for_element_to_be_visible(
        self, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be visible"""
        if not self.wait_for_element_to_be_present(by=by, locator=locator):
            LOGGER.info(f"Locator: {locator} was not present.")

        LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until(EC.visibility_of_element_located((by, locator)))

    def wait_for_element_not_to_be_visible(
        self, by: By, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element NOT to be visible"""
        if not self.wait_for_element_to_be_present(by=by, locator=locator):
            LOGGER.info(f"Locator: {locator} was not present.")

        LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until_not(EC.visibility_of_element_located((by, locator)))
