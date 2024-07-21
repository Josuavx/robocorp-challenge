import re
import os
import csv
from urllib import request

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|,]', '_', filename)

def download_images(results):
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

def save_to_csv(results):
    
    results = clean_results(results)
    
    headers = ['title', 'date', 'description', 'picture_filename', 'search_phrase_count', 'contains_money']
    file_path = os.path.join('data', 'results.csv')
    
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        writer.writeheader()
        
        for result in results:
            writer.writerow(result)
            
            
def clean_results(results):
    for result in results:
        result.pop('picture_url', None)

    return results