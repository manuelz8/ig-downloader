from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
from uuid import uuid4
import json
import os

def get_instagram_media(url) -> dict:

    response = {
        'success': False,
        'media_url': '',
        'username': '',
        'followers': '',
    }

    user_profile_url = ''

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service()

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        TIME_OUT = 5
        CSS_MEDIA_SELECTOR = 'video, img[src*="instagram"]'
        ELEMENT_SELECTOR = (By.CSS_SELECTOR, CSS_MEDIA_SELECTOR)
        WebDriverWait(driver, TIME_OUT)\
            .until(EC.presence_of_element_located(ELEMENT_SELECTOR))

        media_element = driver.find_element(By.CSS_SELECTOR, CSS_MEDIA_SELECTOR)

        media_url = media_element.get_attribute('src')
        response_request = requests.get(media_url)

        # Return if media is not found
        if response_request.status_code != 200:
            return response

        media_type = media_element.tag_name
        extension = 'jpg' if media_type == 'img' else 'mp4'
        filename = f'static/image_folder/{uuid4()}_ig.{extension}'
        with open(filename, 'wb') as media_file:
            media_file.write(response_request.content)

        user_element = driver.find_element(By.CSS_SELECTOR, 'header a')
        anchor_href = user_element.get_attribute('href')
        username = anchor_href.split('/')[-2]

        user_profile_url = anchor_href

    except Exception as e:
        print(e)
        print('Error downloading media.')
        return response
    finally:
        driver.quit()
        response['username'] = username
        response['media_url'] = filename

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(user_profile_url)

        CSS_FOLLOWERS_SELECTOR = 'ul'
        ELEMENT_SELECTOR = (By.CSS_SELECTOR, CSS_FOLLOWERS_SELECTOR)
        WebDriverWait(driver, TIME_OUT)\
            .until(EC.presence_of_element_located(ELEMENT_SELECTOR))

        list_user_data = driver.find_element(By.CSS_SELECTOR, CSS_FOLLOWERS_SELECTOR)
        followers_element = list_user_data.find_element(By.CSS_SELECTOR, 'span[title]')
        followers = followers_element.get_attribute('title')
        response['followers'] = followers

    except Exception as e:
        print(e)
        print('Error reading followers.')
        return response
    finally:
        driver.quit()

    response['success'] = True
    return response

def instagram_audit(new_data):

    FILE_PATH = "static/image_folder/instagram_audit.json"

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

        if not isinstance(existing_data, list):
            existing_data = []

        existing_data.append(new_data)

        with open(FILE_PATH, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open(FILE_PATH, 'w') as file:
            json.dump([new_data], file, indent=4)
