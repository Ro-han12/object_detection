import os
import requests
from bs4 import BeautifulSoup
import urllib.request

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

def download_images(image_urls, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for i, url in enumerate(image_urls, start=1):
        file_name = os.path.join(target_folder, f"image_{i}.jpg")
        try:
            urllib.request.urlretrieve(url, file_name)
            print(f"Image {i} downloaded successfully")
        except Exception as e:
            print(f"Error downloading image {i}: {e}")

def scrape_images(search_url, number_images):
    image_urls = fetch_image_urls(search_url, number_images)
    target_folder = './scraped_images'
    download_images(image_urls, target_folder)

search_url = 'https://www.google.com/search?sca_esv=781fa1a7ec643214&sca_upv=1&rlz=1C5MACD_enIN1079IN1080&sxsrf=ACQVn09uL7oPlPQsRwSVQmHtwf48LD3MpQ:1711115469601&q=hand+palm&tbm=isch&source=lnms&prmd=isvnmbtz&sa=X&ved=2ahUKEwiXx_DtgYiFAxUnSGcHHRSACJcQ0pQJegQIHRAB&biw=1440&bih=779&dpr=2'
number_images = 50
scrape_images(search_url, number_images)
