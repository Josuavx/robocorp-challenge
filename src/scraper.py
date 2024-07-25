import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from src.utils import sanitize_filename

class Scraper:
    """Scraper class for extracting news information from a website."""

    def __init__(self, browser, config: dict, log):
        """Initialize the Scraper with a browser, configuration, and logger.

        Args:
            browser: An instance of BrowserManager.
            config: A dictionary containing configuration settings.
            log: An instance of Logger for logging.
        """
        self.browser = browser
        self.search_phrase = config.get("search_phrase", "")
        self.news_category = config.get("news_category", "")
        self.months = config.get("months", [])
        self.log = log
        self.results = []
        self.pages = 0

    def search_news(self) -> None:
        """Perform a news search based on the search phrase."""
        self.log.info('Searching for news')

        search_button_xpath = "//button[@data-element='search-button']"
        input_xpath = "//input[@data-element='search-form-input']"
        submit_search_button_xpath = "//button[@data-element='search-submit-button']"

        search_button = self.browser.wait_element(By.XPATH, search_button_xpath)
        search_button.click()

        search_input = self.browser.wait_be_clickable(By.XPATH, input_xpath)
        search_input.clear()
        search_input.send_keys(self.search_phrase)

        submit_button = self.browser.wait_element(By.XPATH, submit_search_button_xpath)
        submit_button.click()

    def sort_search(self, option: str) -> None:
        """Sort the search results by the specified option.

        Args:
            option: The sorting option (e.g., 'Newest').
        """
        self.log.info('Applying filters')
        newest_option_xpath = f'//select[@class="select-input"]/option[text()="{option}"]'

        option_newest = self.browser.wait_element(By.XPATH, newest_option_xpath)
        option_newest.click()

    def choose_topic(self) -> None:
        """Select the news category from the available options."""
        checkbox_topic_xpath = f'//div[@class="checkbox-input"]/label/span[text()="{self.news_category}"]/../input'

        checkbox_topic = self.browser.wait_element(By.XPATH, checkbox_topic_xpath)
        checkbox_topic.click()

    def collect_news(self) -> None:
        """Collect news articles from the search results."""
        self.log.info('Collecting news')

        news_list_element_xpath = "//ul[@class='search-results-module-results-menu']"

        while True:
            news_list = self.browser.wait_element(By.XPATH, news_list_element_xpath)
            news_elements = news_list.find_elements(By.XPATH, ".//ps-promo[@class='promo promo-position-large promo-medium']/div")

            for new in news_elements:
                title_xpath = ".//div[@class='promo-content']/div[@class='promo-title-container']/h3/a"
                date_xpath = ".//div[@class='promo-content']/p[@class='promo-timestamp']"
                description_xpath = ".//div[@class='promo-content']/p[@class='promo-description']"
                picture_filename_xpath = ".//div[@class='promo-media']/a/picture/img"

                self.browser.driver.execute_script("arguments[0].scrollIntoView();", new)

                title = new.find_element(By.XPATH, title_xpath).get_attribute('textContent')
                date = new.find_element(By.XPATH, date_xpath).get_attribute('textContent')
                description = new.find_element(By.XPATH, description_xpath).get_attribute('textContent')
                picture_filename = new.find_element(By.XPATH, picture_filename_xpath).get_attribute('alt')
                picture_url = new.find_element(By.XPATH, picture_filename_xpath).get_attribute('src')

                search_phrase_count = self.count_search_phrase(title, description)
                contains_money = self.contains_currency(title, description)

                self.create_news_data(title, date, description, picture_filename, picture_url, search_phrase_count, contains_money)

            if not self.go_to_next_page():
                break

    def create_news_data(self, title: str, date: str, description: str, picture_filename: str, picture_url: str, search_phrase_count: int, contains_money: bool) -> None:
        """Create and store news data from the collected information.

        Args:
            title: The title of the news article.
            date: The date of the news article.
            description: The description of the news article.
            picture_filename: The filename of the news article's picture.
            picture_url: The URL of the news article's picture.
            search_phrase_count: The count of search phrase occurrences in the title and description.
            contains_money: Whether the article contains information about money.
        """
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

    def go_to_next_page(self) -> bool:
        """Navigate to the next page of search results.

        Returns:
            True if the next page exists and was navigated to, False otherwise.
        """
        next_button_xpath = "//div[@class='search-results-module-next-page']/a"

        try:
            next_button = self.browser.wait_be_clickable(By.XPATH, next_button_xpath)
            next_button.click()

            self.pages += 1
            self.log.info(f'Going to page {self.pages}')

            return True
        except TimeoutException:
            self.log.info("There isn't a next page.")
            return False

    def count_search_phrase(self, title: str, description: str) -> int:
        """Count occurrences of the search phrase in the title and description.

        Args:
            title: The title of the news article.
            description: The description of the news article.

        Returns:
            The total count of search phrase occurrences.
        """
        search_phrase_lower = self.search_phrase.lower()
        title_lower = title.lower()
        description_lower = description.lower()

        count_in_title = title_lower.count(search_phrase_lower)
        count_in_description = description_lower.count(search_phrase_lower)

        return count_in_title + count_in_description

    def contains_currency(self, title: str, description: str) -> bool:
        """Check if the title or description contains currency information.

        Args:
            title: The title of the news article.
            description: The description of the news article.

        Returns:
            True if currency information is found, False otherwise.
        """
        text = (title + description).lower().replace(' ', '')

        if '$' in text:
            index = text.find('$')
            text_slice = text[index + 1:]
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

    def get_results(self) -> list:
        """Get the collected news results.

        Returns:
            A list of dictionaries containing news data.
        """
        return self.results
