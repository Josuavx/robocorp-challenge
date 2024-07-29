import os

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from RPA.Browser.Selenium import Selenium

from .wait_manager import WaitManager
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
        submit_search_button_xpath = "//button[@data-element='search-submit-button']"

        self.browser.click_element(search_button_xpath)
        self.browser.input_text(input_xpath, self.search_phrase)
        self.browser.click_element(submit_search_button_xpath)

    def sort_search(self, option):
        self.log.info('Applying filters')

        select_element_xpath = "//select[@class='select-input']"
        self.browser.wait_until_element_is_visible(select_element_xpath, timeout=60)
        self.browser.select_from_list_by_value(select_element_xpath, option)

    def choose_topic(self):
        checkbox_topic_xpath = (
            f'//div[@class="checkbox-input"]/label/span[text()="{self.news_category}"]/../input'
        )

        try:
            self.wait.wait_element(By.XPATH, checkbox_topic_xpath)
            self.scroll_to(checkbox_topic_xpath)
            self.browser.wait_and_click_button(checkbox_topic_xpath)
        except (NoSuchElementException, TimeoutException):
            self.log.info('Checkbox topic not found on page.')

    def collect_news(self):
        self.log.info('Collecting news')

        news_list_element_xpath = "//ul[@class='search-results-module-results-menu']"

        while True:
            self.browser.wait_until_element_is_visible(news_list_element_xpath)
            news_list = self.browser.get_webelement(news_list_element_xpath)
            news_elements = news_list.find_elements(
                By.XPATH, ".//ps-promo[@class='promo promo-position-large promo-medium']/div"
            )

            for index, news_element in enumerate(news_elements):
                self._collect_single_news(news_element, index)

            if not self._go_to_next_page():
                break

    def _collect_single_news(self, news_element, index):
        title_xpath = ".//div[@class='promo-content']/div[@class='promo-title-container']/h3/a"
        date_xpath = ".//div[@class='promo-content']/p[@class='promo-timestamp']"
        description_xpath = ".//div[@class='promo-content']/p[@class='promo-description']"
        picture_filename_xpath = ".//div[@class='promo-media']/a/picture/img"

        self.scroll_to(title_xpath)

        try:
            self.log.info(f'Collecting news {index} on this page.')
            self.wait.wait_element(By.XPATH, title_xpath)
            title = news_element.find_element(By.XPATH, title_xpath).get_attribute('textContent')

            self.wait.wait_element(By.XPATH, date_xpath)
            date = news_element.find_element(By.XPATH, date_xpath).get_attribute('textContent')

            self.wait.wait_element(By.XPATH, description_xpath)
            description = news_element.find_element(By.XPATH, description_xpath).get_attribute('textContent')

            self.wait.wait_element(By.XPATH, picture_filename_xpath)
            picture_filename = news_element.find_element(By.XPATH, picture_filename_xpath).get_attribute('alt')
            picture_url = news_element.find_element(By.XPATH, picture_filename_xpath).get_attribute('src')
        except (NoSuchElementException, TimeoutException):
            self.log.info(f'Skipping news {index}. Element not found.')
            return

        search_phrase_count = self._count_search_phrase(title, description)
        contains_money = self._contains_currency(title, description)

        self._create_news_data(title, date, description, picture_filename, picture_url, search_phrase_count, contains_money)

    def _create_news_data(self, title, date, description, picture_filename, picture_url, search_phrase_count, contains_money):
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

    def _go_to_next_page(self):
        next_button_xpath = "//div[@class='search-results-module-next-page']/a"

        try:
            self.browser.click_element(next_button_xpath)
            self.pages += 1
            self.log.info(f'Going to page {self.pages}')
            return True
        except Exception:
            self.log.info("There isn't a next page.")
            return False

    def _count_search_phrase(self, title, description):
        search_phrase_lower = self.search_phrase.lower()
        title_lower = title.lower()
        description_lower = description.lower()

        count_in_title = title_lower.count(search_phrase_lower)
        count_in_description = description_lower.count(search_phrase_lower)

        return count_in_title + count_in_description

    def _contains_currency(self, title, description):
        text = (title + description).lower().replace(' ', '')

        if '$' in text:
            index = text.find('$')
            if text[index + 1].isdigit():
                return True

        if 'dollars' in text:
            index = text.find('dollars')
            if text[index - 1].isdigit():
                return True

        if 'usd' in text:
            index = text.find('usd')
            if text[index - 1].isdigit():
                return True

        return False

    def scroll_to(self, xpath):
        self.browser.execute_javascript(
            f"""
            var xpath = "{xpath}";
            var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            var element = result.singleNodeValue;
            if (element) {{
                element.scrollIntoView(true);
            }}
            """
        )

    def get_results(self):
        return self.results

    def get_months(self):
        return self.months
