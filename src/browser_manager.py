from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .wait_manager import WaitManager

class BrowserManager(WaitManager):
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        super().__init__(driver)
    
    def start(self, url):
        self.driver.get(url)
    
    def close(self):
        self.driver.quit()

    