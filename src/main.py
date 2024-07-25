import json
import traceback
from time import sleep

from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from src.utils import save_to_csv, download_images
from src.browser_manager import BrowserManager
from src.scraper import Scraper
from src.logger import Logger

def load_config(file_path: str) -> dict:
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config
@task
def search_and_store() -> None:
    """Main task to search news, download images, and save results."""
    browser = BrowserManager()  # Initializes the browser manager
    try:
        config = load_config('config/config.json')
        
        logger_instance = Logger(__name__)
        log = logger_instance.get_logger()
        
        browser.start('https://www.latimes.com/')
        
        scraper = Scraper(browser.browser, config, log)  # Pass the browser instance to Scraper
        
        scraper.search_news()
        scraper.sort_search('1')
        sleep(2)
        scraper.choose_topic()
        sleep(2)
        scraper.collect_news()
        
        results = scraper.get_results()
        
        log.info('Downloading news images.')
        download_images(results)
        
        log.info('Saving results to .csv file.')
        save_to_csv(results)
        
    except Exception as e:
        log.error(f'An error occurred: {e}')
        traceback.print_exc()
        sleep(60)
    finally:
        browser.close()
