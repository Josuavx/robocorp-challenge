import csv
import os
import re
from urllib import request
from typing import List, Dict
from robocorp import workitems

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by replacing invalid characters with underscores.

    Args:
        filename: The original filename.

    Returns:
        A sanitized version of the filename.
    """
    return re.sub(r'[\\/:"*?<>|,]', '_', filename)

def download_images(results: List[Dict[str, str]]) -> None:
    """Download images based on the provided results.

    Args:
        results: A list of dictionaries containing image URLs and filenames.
    """
    for data in results:
        try:
            directory = os.path.dirname(data['picture_filename'])
            
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with request.urlopen(data['picture_url']) as response:
                image_data = response.read()
                with open(data['picture_filename'], 'wb') as file:
                    file.write(image_data)
        except Exception as e:
            print(f"Error downloading image: {e}")

def save_to_csv(results: List[Dict[str, str]]) -> None:
    """Save results to a CSV file after cleaning.

    Args:
        results: A list of dictionaries containing news data.
    """
    results = clean_results(results)
    
    headers = ['title', 'date', 'description', 'picture_filename', 'search_phrase_count', 'contains_money']
    file_path = os.path.join('data', 'results.csv')
    
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)
    
    add_csv_as_output(file_path)
            
def clean_results(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove the 'picture_url' key from each result.

    Args:
        results: A list of dictionaries containing news data.

    Returns:
        A cleaned list of dictionaries without 'picture_url' key.
    """
    for result in results:
        result.pop('picture_url', None)

    return results

def add_csv_as_output(file_path: str) -> None:
    workitems.outputs.create(
        payload={"key": "value"},
        files=[file_path],
    )