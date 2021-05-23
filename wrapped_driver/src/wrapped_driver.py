"""wrapped_driver.py

Module for all webdriver classes and methods
"""
import logging
from sys import stdout
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


LOGGER_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOGGER_FORMAT,
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


def get_chrome_options() -> webdriver.ChromeOptions:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    return chrome_options


def get_firefox_options() -> webdriver.FirefoxOptions:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--disable-features=VizDisplayCompositor")
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--disable-gpu")
    return firefox_options


class WrappedDriver:
    """Class used to wrap selenium webdriver"""

    def __init__(
        self,
        executable_path: str,
        browser: str = "chrome",
        headless: bool = False,
        mobile: bool = False,
        user_agent: str = USER_AGENT,
        window_size: tuple = None,
    ):
        self.options = (
            get_firefox_options() if browser == "firefox" else get_chrome_options()
        )
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--no-sandbox")

        if window_size:
            width, height = window_size
            self.options.add_argument(f"--window-size={width},{height}")

        if mobile:
            self.options.add_argument(MOBILE_USER_AGENT)
        else:
            self.options.add_argument(user_agent)
            if not window_size:
                self.options.add_argument("--window-size=1920,1080")

        if browser == "chrome":
            self.driver = webdriver.Chrome(
                executable_path=executable_path, options=self.options
            )
        elif browser == "firefox":
            self.driver = webdriver.Firefox(
                executable_path=executable_path, options=self.options
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

    def element_exist(self, locator: str = None, element: WebElement = None) -> bool:
        """Return bool for element visibility"""
        try:
            if not element:
                element = self.get_element_by_css(locator)
            return element.is_displayed()
        except NoSuchElementException as e:
            LOGGER.debug(e)
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
        return self.driver.find_element_by_id(element_id)

    def get_elements_by_id(self, element_id: str) -> List[WebElement]:
        return self.driver.find_elements_by_id(element_id)

    def get_element_by_css(self, locator: str) -> WebElement:
        return self.driver.find_element_by_css_selector(css_selector=locator)

    def get_elements_by_css(self, locator: str) -> List[WebElement]:
        return self.driver.find_elements_by_css_selector(css_selector=locator)

    def get_element_by_text(self, text: str) -> WebElement:
        return self.driver.find_element_by_xpath(xpath=f"//*[text()='{text}']")

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
        LOGGER.debug(f"Scrolling to WebElement: {element}")
        ActionChains(self.driver).move_to_element(element).perform()

    @property
    def switch_to(self):
        """Wrapped method of selenium webdriver switch_to"""
        return self.driver.switch_to

    @property
    def title(self) -> str:
        return self.driver.title

    def wait_for_element_to_be_present(
        self, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present"""
        LOGGER.debug(msg=f"Waiting for locator to be present: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until(EC.presence_of_element_located((by, locator)))

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

    def wait_for_element_to_be_present_by_id(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using ID locator"""
        return self.wait_for_element_to_be_present(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_not_to_be_present(
        self, by: By, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to not be present"""
        LOGGER.debug(msg=f"Waiting for locator to NOT be present: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until_not(EC.presence_of_element_located((by, locator)))

    def wait_for_element_not_to_be_present_by_css(
        self, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element not to be present using CSS locator"""
        return self.wait_for_element_not_to_be_present(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_not_to_be_present_by_id(
        self, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element not to be present using ID locator"""
        return self.wait_for_element_not_to_be_present(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

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

    def wait_for_element_to_be_visible_by_css(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be visible using CSS locator"""
        return self.wait_for_element_to_be_visible(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_visible_by_id(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be visible using ID locator"""
        return self.wait_for_element_to_be_visible(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

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

    def wait_for_element_not_to_be_visible_by_id(
        self, locator: str, timeout: int = 5, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using ID locator"""
        return self.wait_for_element_not_to_be_visible(
            by=By.ID,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )
