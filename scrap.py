import os
import requests
from bs4 import BeautifulSoup
import re

def fetch_image_urls(search_url, number_images):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = []
    for img in soup.find_all('img', src=True):
        image_url = img['src']
        if image_url.startswith('http'):
            image_urls.append(image_url)
            if len(image_urls) == number_images:
                break
    return image_urls

def persist_image(folder_path, url, counter):
    try:
        image_content = requests.get(url).content
        with open(os.path.join(folder_path, f"image_{counter}.jpg"), 'wb') as f:
            f.write(image_content)
        print(f"Image {counter} downloaded successfully")
    except Exception as e:
        print(f"Error downloading image {counter}: {e}")

def scrape_images(search_url, number_images):
    image_urls = fetch_image_urls(search_url, number_images)
    target_folder = './scraped_images'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for i, url in enumerate(image_urls, start=1):
        persist_image(target_folder, url, i)

search_url = 'https://www.google.com/search?sca_esv=781fa1a7ec643214&sca_upv=1&rlz=1C5MACD_enIN1079IN1080&sxsrf=ACQVn09uL7oPlPQsRwSVQmHtwf48LD3MpQ:1711115469601&q=hand+palm&tbm=isch&source=lnms&prmd=isvnmbtz&sa=X&ved=2ahUKEwiXx_DtgYiFAxUnSGcHHRSACJcQ0pQJegQIHRAB&biw=1440&bih=779&dpr=2'
number_images = 50
scrape_images(search_url, number_images)
