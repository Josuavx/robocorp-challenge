from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple

class WaitManager:
    """A class to manage waiting for elements in Selenium WebDriver."""

    def __init__(self, driver, timeout: int = 10):
        """Initialize the WaitManager with a driver and timeout.

        Args:
            driver: An instance of Selenium WebDriver.
            timeout: The maximum amount of time (in seconds) to wait for an element.
        """
        self.driver = driver
        self.timeout = timeout

    def wait_element(self, by: By, value: str) -> object:
        """Wait for the presence of an element located by the specified method.

        Args:
            by: The method to locate the element (e.g., By.XPATH).
            value: The value of the locator.

        Returns:
            The located WebElement.
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_be_clickable(self, by: By, value: str) -> object:
        """Wait for an element to be clickable.

        Args:
            by: The method to locate the element (e.g., By.XPATH).
            value: The value of the locator.

        Returns:
            The clickable WebElement.
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_visibility(self, by: By, value: str) -> object:
        """Wait for an element to be visible.

        Args:
            by: The method to locate the element (e.g., By.XPATH).
            value: The value of the locator.

        Returns:
            The visible WebElement.
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((by, value))
        )
