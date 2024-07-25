from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.wait_manager import WaitManager

class BrowserManager(WaitManager):
    """BrowserManager class for managing the browser instance."""

    def __init__(self):
        """Initialize the BrowserManager with a Chrome browser instance."""
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        super().__init__(driver)

    def start(self, url: str) -> None:
        """Navigate to the specified URL in the browser."""
        self.driver.get(url)

    def close(self) -> None:
        """Close the browser and quit the driver."""
        self.driver.quit()
