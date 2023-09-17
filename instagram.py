from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
from uuid import uuid4

def get_instagram_media(url):

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'video')))

        media_element = driver.find_element(By.CSS_SELECTOR, 'video')

        media_url = media_element.get_attribute('src')

        filename = f'static/image_folder/{uuid4()}_ig.mp4'

        response = requests.get(media_url)

        if response.status_code == 200:
            with open(filename, 'wb') as media_file:
                media_file.write(response.content)
            return filename
        else:
            return 'Failed to download media.'
    except Exception as e:
        print('Error downloading video trying with image')
    finally:
        driver.quit()

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="instagram"]')))

        media_element = driver.find_element(By.CSS_SELECTOR, 'img[src*="instagram"]')

        media_url = media_element.get_attribute('src')

        filename = f'static/image_folder/{uuid4()}_ig.jpg'

        response = requests.get(media_url)

        if response.status_code == 200:
            with open(filename, 'wb') as media_file:
                media_file.write(response.content)
            return filename
        else:
            print("Failed to download media.")
    except Exception as e:
        print('Error downloading image')
    finally:
        driver.quit()

    return 'Failed to download media.'