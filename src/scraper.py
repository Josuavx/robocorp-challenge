from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import BrowserManagementKeywords
from RPA.Browser.Selenium import SeleniumLibrary
from .wait_manager import WaitManager
from selenium.webdriver.common.by import By
import os
from src.utils import sanitize_filename

class Scraper:
    def __init__(self, browser: Selenium, config: dict, log):
        self.browser = browser
        self.search_phrase = config.get("search_phrase")
        self.news_category = config.get("news_category")
        self.months = config.get("months")
        self.log = log
        self.results = []
        self.pages = 0
        self.wait = WaitManager(self.browser, 60)

    def search_news(self):
        self.log.info('Searching for news')

        search_button_xpath = "//button[@data-element='search-button']"
        input_xpath = "//input[@data-element='search-form-input']"
        submit_search_button = "//button[@data-element='search-submit-button']"

        # Find and click the search button
        self.browser.click_element(search_button_xpath)

        # Enter the search phrase
        self.browser.input_text(input_xpath, self.search_phrase)

        # Submit the search form
        self.browser.click_element(submit_search_button)

    def sort_search(self, option):
        self.log.info('Applying filters')

        # Select the option from the dropdown
        select_element_xpath = "//select[@class='select-input']"
        self.browser.wait_until_element_is_visible(select_element_xpath, timeout=60)
        self.browser.select_from_list_by_value(select_element_xpath, option)

    def choose_topic(self):
        checkbox_topic_xpath = f'//div[@class="checkbox-input"]/label/span[text()="{self.news_category}"]/../input'

        # Click the checkbox to choose the topic
        self.browser.wait_until_element_is_visible(checkbox_topic_xpath, timeout=60)
        self.browser.wait_and_click_button(checkbox_topic_xpath)

    def collect_news(self):
        self.log.info('Collecting news')

        news_list_element_xpath = "//ul[@class='search-results-module-results-menu']"

        while True:
            self.browser.wait_until_element_is_visible(news_list_element_xpath)
            news_list = self.browser.get_webelement(news_list_element_xpath)
            news_elements = news_list.find_elements(By.XPATH, ".//ps-promo[@class='promo promo-position-large promo-medium']/div")

            for index, new in enumerate(news_elements):
                title_xpath = ".//div[@class='promo-content']/div[@class='promo-title-container']/h3/a"
                date_xpath = ".//div[@class='promo-content']/p[@class='promo-timestamp']"
                description_xpath = ".//div[@class='promo-content']/p[@class='promo-description']"
                picture_filename_xpath = ".//div[@class='promo-media']/a/picture/img"

                # Scroll to the news element
                self.browser.execute_javascript(
                    """
                    var xpath = "//div[@class='promo-content']/div[@class='promo-title-container']/h3/a";
                    var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    var element = result.singleNodeValue;
                    if (element) {
                        element.scrollIntoView(true);
                    }
                    """
            )
                
                self.log.info(f'Init {index}')
                self.wait.wait_element(By.XPATH, title_xpath)
                title = new.find_element(By.XPATH, title_xpath).get_attribute('textContent')
                self.log.info('Title ok')
                self.browser.wait_until_element_is_visible(date_xpath, timeout=300)
                date = new.find_element(By.XPATH, date_xpath).get_attribute('textContent')
                self.log.info('Date ok')
                self.browser.wait_until_element_is_visible(description_xpath, timeout=300)
                description = new.find_element(By.XPATH, description_xpath).get_attribute('textContent')
                self.log.info('Description ok')
                self.browser.wait_until_element_is_visible(picture_filename_xpath, timeout=300)
                picture_filename = new.find_element(By.XPATH, picture_filename_xpath).get_attribute('alt')
                self.log.info('filename ok')
                picture_url = new.find_element(By.XPATH, picture_filename_xpath).get_attribute('src')
                self.log.info('url ok')

                search_phrase_count = self.count_search_phrase(title, description)
                contains_money = self.contains_currency(title, description)

                self.create_news_data(title, date, description, picture_filename, picture_url, search_phrase_count, contains_money)

            if not self.go_to_next_page():
                break

    def create_news_data(self, title, date, description, picture_filename, picture_url, search_phrase_count, contains_money):
        picture_filename = sanitize_filename(picture_filename)[:100] + '.png'
        picture_filename = os.path.join(os.getcwd(), 'images', picture_filename)

        news_data = {
            'title': title,
            'date': date,
            'description': description,
            'picture_filename': picture_filename,
            'picture_url': picture_url.split(' ')[0],
            'search_phrase_count': search_phrase_count,
            'contains_money': contains_money
        }

        self.results.append(news_data)

    def go_to_next_page(self):
        next_button_xpath = "//div[@class='search-results-module-next-page']/a"

        try:
            self.browser.click_element(next_button_xpath)
            self.pages += 1
            self.log.info(f'Going to page {self.pages}')
            return True
        except Exception:
            self.log.info("There isn't a next page.")
            return False

    def count_search_phrase(self, title, description):
        search_phrase_lower = self.search_phrase.lower()
        title_lower = title.lower()
        description_lower = description.lower()

        count_in_title = title_lower.count(search_phrase_lower)
        count_in_description = description_lower.count(search_phrase_lower)

        return count_in_title + count_in_description

    def contains_currency(self, title, description):
        text = title + description
        text = text.lower().replace(' ', '')

        if '$' in text:
            index = text.find('$')
            text_slice = text[index+1:]

            if text_slice and text_slice[0].isdigit():
                return True

        if 'dollars' in text:
            index = text.find('dollars')
            text_slice = text[:index]

            if text_slice and text_slice[-1].isdigit():
                return True

        if 'usd' in text:
            index = text.find('usd')
            text_slice = text[:index]

            if text_slice and text_slice[-1].isdigit():
                return True

        return False

    def get_results(self):
        return self.results
