from robocorp.tasks import task
from .browser_manager import BrowserManager
from .scraper import Scraper
from .logger import Logger
from time import sleep
from src.utils import save_to_csv, download_images
import traceback
import json


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

@task
def search_and_store():
    try:
        config = load_config('config/config.json')
        
        logger_instance = Logger(__name__)
        log = logger_instance.get_logger()
        
        browser = BrowserManager()
        scraper = Scraper(browser, config, log)

        browser.start('https://www.latimes.com/')
        
        scraper.search_news()
        
        scraper.sort_search('Newest')
        sleep(2)
        scraper.choose_topic()
        sleep(2)
        scraper.collect_news()
        
        results = scraper.get_results()
        
        log.info('Downloading news')
        download_images(results)
        
        log.info('Saving .csv file')
        save_to_csv(results)
        
    except Exception:
        traceback.print_exc()
        sleep(60)
        browser.close()