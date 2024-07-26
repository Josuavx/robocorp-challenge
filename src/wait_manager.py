from RPA.Browser.Selenium import Selenium
from typing import Tuple

class WaitManager:
    """A class to manage waiting for elements in RPA Framework."""

    def __init__(self, browser: Selenium, timeout: int = 10) -> None:
        """Initialize the WaitManager with a browser and timeout.

        Args:
            browser: An instance of Selenium browser from RPA Framework.
            timeout: The maximum amount of time (in seconds) to wait for an element.
        """
        self.browser = browser
        self.timeout = timeout

    def wait_element(self, by: str, value: str) -> None:
        """Wait for the presence of an element located by the specified method."""
        self.browser.wait_until_element_is_visible(f"{by}={value}")

    def wait_be_clickable(self, by: str, value: str) -> None:
        """Wait for an element to be clickable."""
        self.browser.wait_until_element_is_clickable(f"{by}={value}")

    def wait_for_visibility(self, by: str, value: str) -> None:
        """Wait for an element to be visible."""
        self.browser.wait_until_element_is_visible(f"{by}={value}")
