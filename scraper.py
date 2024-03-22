from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import requests

def fetch_image_urls(search_term, number_images, wd=None, sleep_between_interactions=0.5):
    search_url = f"https://www.google.com/search?q={search_term}&tbm=isch"
    wd.get(search_url)
    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < number_images:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        number_results = len(thumbnail_results)
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
            image_count = len(image_urls)
            if len(image_urls) >= number_images:
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)  # Adjust if needed
            return  # Return to exit the function if more images are not found
            load_more_button = wd.find_element(By.CSS_SELECTOR, ".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
        results_start = len(thumbnail_results)
    return image_urls


def persist_image(folder_path:str,url:str,counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        return  # Return if image download fails
    
    try:
        image_file = os.path.join(folder_path, f"{counter}.jpg")
        with open(image_file, 'wb') as f:
            f.write(image_content)
        print(f"SUCCESS - saved {url} - as {image_file}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term:str, driver_path:str, target_folder='./images', number_images=5):
    # Create target folder if it doesn't exist
    target_folder = os.path.join(target_folder, '_'.join(search_term.lower().split(' ')))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Initialize Chrome WebDriver
    with webdriver.Chrome() as wd:
        # Fetch image URLs
        image_urls = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    # Persist images
    for counter, url in enumerate(image_urls):
        persist_image(target_folder, url, counter)

# Set the path to the directory containing the Chrome WebDriver executable
DRIVER_PATH = '/Users/rohansridhar/Desktop/cv/object_detection/chromedriver'

# Set the search term and the number of images to download
search_term = 'hand palm'
number_images = 50

# Call the function to search and download images
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=number_images)
