from RPA.Browser.Selenium import Selenium


class BrowserManager:
    def __init__(self) -> None:
        self.browser = Selenium()

    def start(self, url: str) -> None:
        """Open a URL in the browser."""
        self.browser.open_chrome_browser(url, maximized=True, headless=True)

    def close(self) -> None:
        """Close the browser."""
        self.browser.close_browser()
