import csv
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib import request

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

def save_to_csv(results: List[Dict[str, str]], months: int) -> None:
    """Save results to a CSV file after filtering and cleaning.

    Args:
        results: A list of dictionaries containing news data.
        months: The number of months to filter the results by.
    """
    filtered_results = filter_by_date(results, months)
    filtered_results = clean_results(filtered_results)
    print(filtered_results)
    headers = ['title', 'date', 'description', 'picture_filename', 'search_phrase_count', 'contains_money']
    file_path = os.path.join('data', 'results.csv')
    
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered_results)
    
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
    """Add CSV file as output."""
    workitems.outputs.create(
        payload={"results": "True"},
        files=[file_path],
    )

def filter_by_date(results: List[Dict[str, str]], months: int) -> List[Dict[str, str]]:
    """Filter news results based on the number of months provided.

    Args:
        results: A list of dictionaries containing news data.
        months: The number of months from the current date to include in the results.

    Returns:
        A filtered list of dictionaries containing only news within the specified date range.
    """
    today = datetime.now()
    start_date = today - timedelta(days=months * 30)  # Rough estimate: 30 days per month

    def parse_date(date_str: str) -> Optional[datetime]:
        """Parse a date string in the format 'Month Day, Year'."""
        try:
            return datetime.strptime(date_str, '%B %d, %Y')
        except ValueError:
            return None

    def is_time_sensitive(description: str) -> bool:
        """Check if the description contains time-sensitive keywords."""
        time_keywords = ['hour', 'hours', 'minute', 'minutes']
        return any(keyword in description.lower() for keyword in time_keywords)

    filtered_results = []
    for result in results:
        date_str = result.get('date')
        date_obj = parse_date(date_str)
        description = result.get('description', '')

        if (date_obj and start_date <= date_obj <= today) or is_time_sensitive(description):
            filtered_results.append(result)
    
    return filtered_results