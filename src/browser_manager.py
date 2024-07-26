from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options

class BrowserManager:
    def __init__(self) -> None:
        self.browser = Selenium()

    def start(self, url: str) -> None:
        """Open a URL in the browser."""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        self.browser.open_browser(url, browser='chrome', options=chrome_options)

    def close(self) -> None:
        """Close the browser."""
        self.browser.close_browser()
