from RPA.Browser.Selenium import Selenium

class BrowserManager:
    def __init__(self) -> None:
        self.browser = Selenium()

    def start(self, url: str) -> None:
        """Open a URL in the browser."""
        # Configurar o navegador com opções específicas, se necessário
        self.browser.open_browser(url, browser='chrome')  # Argumento 'headless' não é usado diretamente aqui

    def close(self) -> None:
        """Close the browser."""
        self.browser.close_browser()
