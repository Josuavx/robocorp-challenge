from robocorp.tasks import task
from .browser_manager import BrowserManager
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

        browser = BrowserManager()
        
        browser.start('https://www.latimes.com/')
        
        
    except Exception:
        traceback.print_exc()
        browser.close()