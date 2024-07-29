import json
import os
import traceback
from time import sleep

from robocorp import workitems
from robocorp.tasks import task

from src.browser_manager import BrowserManager
from src.logger import Logger
from src.scraper import Scraper
from src.utils import save_to_csv, download_images


def handle_item():
    try:
        item = workitems.inputs.current
        print("Received payload from Control Room:", item.payload)
        
        config_data = item.payload
        
        if config_data is None:
            return None
        
        os.makedirs(os.path.join(os.getcwd(), 'input'), exist_ok=True)
        
        config_path = os.path.join(os.getcwd(), 'input', 'config.json')
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file)

        workitems.outputs.create(
            payload={"status": "config saved"},
            files=[config_path],
        )
        
        return config_data
    except Exception as e:
        traceback.print_exc()
        return None

def simulate_handle_item():
    try:
        config_path = os.path.join(os.getcwd(), 'input', 'config.json')
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
        
        return config_data
    except Exception as e:
        traceback.print_exc()
        return None

@task
def search_and_store() -> None:
    """Main task to search news, download images, and save results."""
    browser = BrowserManager()  # Initializes the browser manager
    try:
        logger_instance = Logger(__name__)
        log = logger_instance.get_logger()
    
        config = handle_item()
        if config is None:  
            config = simulate_handle_item()
        
        print(config)
        if config is None:  
            raise ValueError("No configuration found.")
        
        log.info(config)
        
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
        save_to_csv(results, scraper.get_months())
        
    except Exception:
        traceback.print_exc()
        sleep(60)
    finally:
        browser.close()
