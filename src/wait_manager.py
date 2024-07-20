from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WaitManager:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def wait_element(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((by, value)))

    def wait_be_clickable(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((by, value)))

    def wait_for_visibility(self, by, value):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((by, value)))