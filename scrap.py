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
    target_folder = './scraped_images2'
    download_images(image_urls, target_folder)

search_url = 'https://www.google.com/search?q=palm++hand+images&sca_esv=e2291660b3e8fe71&sca_upv=1&rlz=1C5MACD_enIN1079IN1080&udm=2&biw=1440&bih=779&sxsrf=ACQVn095r5Trg2sBwa3bN4eMlVVexswcAg%3A1712805109420&ei=9VQXZr2bGa6cseMPs7yauAw&ved=0ahUKEwj96fagmLmFAxUuTmwGHTOeBscQ4dUDCBA&uact=5&oq=palm++hand+images&gs_lp=Egxnd3Mtd2l6LXNlcnAiEXBhbG0gIGhhbmQgaW1hZ2VzMgUQABiABDIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBRgeMgYQABgFGB4yBhAAGAgYHjIGEAAYCBgeMgYQABgIGB4yBhAAGAgYHkivEVDoA1iKC3ABeACQAQCYAWKgAa8EqgEBNrgBA8gBAPgBAZgCB6ACxATCAgoQABiABBiKBRhDwgIIEAAYBRgHGB7CAggQABgIGAcYHpgDAIgGAZIHAzYuMaAH-SQ&sclient=gws-wiz-serp'
number_images = 50
scrape_images(search_url, number_images)
