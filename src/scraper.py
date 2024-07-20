from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, browser, config):
        # self.config = config
        self.browser = browser
        self.search_phrase = config.get("search_phrase")
        self.news_category = config.get("news_category")
        self.months = config.get("months")
        self.results = []

    def search_news(self):
        search_button_xpath = "//button[@data-element='search-button']"
        input_xpath = "//input[@data-element='search-form-input']"
        submit_search_button = "//button[@data-element='search-submit-button']"
        
        search_button = self.browser.wait_element(By.XPATH, search_button_xpath)
        search_button.click()

        search_input = self.browser.wait_be_clickable(By.XPATH, input_xpath) 
        search_input.clear()
        
        search_input.send_keys(self.search_phrase)

        submit_button = self.browser.wait_element(By.XPATH, submit_search_button) 
        submit_button.click()
    
    def collect_news(self):
        news_list_element = "//ul[@class='search-results-module-results-menu']"

        news_list = self.browser.wait_element(By.XPATH, news_list_element) 

        news_elements = news_list.find_elements(By.XPATH, ".//ps-promo[@class='promo promo-position-large promo-medium']/div")

        for index, new in enumerate(news_elements):
            
            title_xpath = ".//div[@class='promo-content']/div[@class='promo-title-container']/h3/a"
            date_xpath = ".//div[@class='promo-content']/p[@class='promo-timestamp']"
            description_xpath = ".//div[@class='promo-content']/p[@class='promo-description']"
            picture_filename_xpath = ".//div[@class='promo-media']/a/picture/img"
            
            self.browser.driver.execute_script("arguments[0].scrollIntoView();", new)

            print(index)
            title = new.find_element(By.XPATH, title_xpath).get_attribute('textContent')
            print(title)
            date = new.find_element(By.XPATH, date_xpath)
            print(date)
            description = new.find_element(By.XPATH, description_xpath).get_attribute('textContent')
            print(description)
            picture_filename = new.find_element(By.XPATH, picture_filename_xpath).get_attribute('textContent')
            print(picture_filename)
            

            # search_phrase_count = ""
            # contains_money = ""
