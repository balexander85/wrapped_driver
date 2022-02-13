"""waits.py

Helper functions for waiting for web elements to be present or nah
"""
import logging
from sys import stdout

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants import LOGGER_FORMAT

logging.basicConfig(
    level=logging.INFO,
    format=LOGGER_FORMAT,
    stream=stdout,
)
WAIT_LOGGER = logging.getLogger(__name__)


def wait_for_element_to_be_present(
    driver: webdriver,
    by: By,
    locator: str,
    timeout: int = 60,
    poll_frequency: int = 3,
) -> bool:
    """Wait for element to be present"""
    WAIT_LOGGER.debug(
        msg=f"Waiting for locator to be present by: {by} locator: {locator}"
    )
    return WebDriverWait(
        driver=driver, timeout=timeout, poll_frequency=poll_frequency
    ).until(ec.presence_of_element_located((by, locator)))


def wait_for_element_to_be_present_by_css(
    driver: webdriver, locator: str, timeout: int = 60, poll_frequency: int = 3
) -> bool:
    """Wait for element to be present using CSS locator"""
    return wait_for_element_to_be_present(
        driver=driver,
        by=By.CSS_SELECTOR,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )


def wait_for_element_to_be_present_by_id(
    driver: webdriver, locator: str, timeout: int = 60, poll_frequency: int = 3
) -> bool:
    """Wait for element to be present using ID locator"""
    return wait_for_element_to_be_present(
        driver=driver,
        by=By.ID,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )


def wait_for_element_not_to_be_present(
    driver: webdriver, by: By, locator: str, timeout: int = 5, poll_frequency: int = 3
) -> bool:
    """Wait for element to not be present"""
    WAIT_LOGGER.debug(msg=f"Waiting for locator to NOT be present: {locator}")
    return WebDriverWait(
        driver=driver, timeout=timeout, poll_frequency=poll_frequency
    ).until_not(ec.presence_of_element_located((by, locator)))


def wait_for_element_not_to_be_present_by_css(
    driver: webdriver, locator: str, timeout: int = 5, poll_frequency: int = 3
) -> bool:
    """Wait for element not to be present using CSS locator"""
    return wait_for_element_not_to_be_present(
        driver=driver,
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
    driver: webdriver, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
) -> bool:
    """Wait for element to be visible"""
    if not wait_for_element_to_be_present(driver=driver, by=by, locator=locator):
        WAIT_LOGGER.info("Locator: %s was not present.", locator)

    WAIT_LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
    return WebDriverWait(
        driver=driver, timeout=timeout, poll_frequency=poll_frequency
    ).until(ec.visibility_of_element_located((by, locator)))


def wait_for_element_to_be_visible_by_css(
    driver: webdriver, locator: str, timeout: int = 60, poll_frequency: int = 3
) -> bool:
    """Wait for element to be visible using CSS locator"""
    return wait_for_element_to_be_visible(
        driver=driver,
        by=By.CSS_SELECTOR,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )


def wait_for_element_to_be_visible_by_id(
    driver: webdriver, locator: str, timeout: int = 60, poll_frequency: int = 3
) -> bool:
    """Wait for element to be visible using ID locator"""
    return wait_for_element_to_be_visible(
        driver=driver,
        by=By.ID,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )


def wait_for_element_not_to_be_visible(
    driver: webdriver, by: By, locator: str, timeout: int = 5, poll_frequency: int = 3
) -> bool:
    """Wait for element NOT to be visible"""
    if not wait_for_element_to_be_present(driver=driver, by=by, locator=locator):
        WAIT_LOGGER.info("Locator: %s was not present.", locator)

    WAIT_LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
    return WebDriverWait(
        driver=driver, timeout=timeout, poll_frequency=poll_frequency
    ).until_not(ec.visibility_of_element_located((by, locator)))


def wait_for_element_not_to_be_visible_by_css(
    driver: webdriver, locator: str, timeout: int = 5, poll_frequency: int = 3
) -> bool:
    """Wait for element to be present using CSS locator"""
    return wait_for_element_not_to_be_visible(
        driver=driver,
        by=By.CSS_SELECTOR,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )


def wait_for_element_not_to_be_visible_by_id(
    driver: webdriver, locator: str, timeout: int = 5, poll_frequency: int = 3
) -> bool:
    """Wait for element to be present using ID locator"""
    return wait_for_element_not_to_be_visible(
        driver=driver,
        by=By.ID,
        locator=locator,
        timeout=timeout,
        poll_frequency=poll_frequency,
    )
