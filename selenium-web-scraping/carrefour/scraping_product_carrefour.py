from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import pytesseract as ocr
from PIL import Image
import numpy as np
import cv2
from bs4 import BeautifulSoup
import json
import datetime
from json import JSONEncoder
import csv
import Repository.productdb as db
from queue import Queue
from _io import BytesIO

q_link = Queue()


class Product():
    def __init__(self, name, price_of, price_per, promotion):
        self.name = name
        self.price_of = price_of
        self.price_per = price_per
        self.promotion = promotion


def remove_str_in_price(price):
    stopwords = ['de:', 'r$', 'por:']
    query_words = price.split()
    resultwords = [word for word in query_words if word.lower()
                   not in stopwords]
    result = ' '.join(resultwords)
    return result


with open('categories.csv') as file:
    csv_reader = csv.DictReader(file, fieldnames=["Name", "Link"])
    csv_reader.__next__()

    for row in csv_reader:
        q_link.put(row["Link"])

        option = webdriver.ChromeOptions()
        option.add_argument(' — incognito')
        driver = webdriver.Chrome(
            executable_path=r'C:\Python\chromedriver.exe', options=option)
        driver.get(q_link.get())

        timeout = 60

        try:
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'prd-thumb')))
        except TimeoutException:
            print('Timed out waiting for page to load')
            driver.quit()

        btn_next_page = driver.find_element_by_id('loadNextPage')

        for x in range(1):
            btn_next_page.click()

        html_content = driver.find_element_by_class_name(
            'category-result-list')
        card_product = html_content.get_attribute('innerHTML')
        soup = BeautifulSoup(card_product, 'html.parser')
        prd_info = soup.find_all(class_='prd-info')

        for prd in prd_info:
            soup_prd = BeautifulSoup(prd.prettify(), 'html.parser')
            extract_bdi = soup_prd.bdi.decompose()
            prd_name = soup_prd.find(class_='prd-name').get_text(strip=True)
            product = Product(prd_name, None, None, None)
            for data in soup_prd:
                prd_price_of = soup_prd.find(class_='prd-price-old')
                if prd_price_of is not None:
                    price_of = prd_price_of.get_text(strip=True)
                    product.price_of = remove_str_in_price(price_of)
                prd_price_per = soup_prd.find(class_='prd-price-new')
                if prd_price_per is not None:
                    price_per = prd_price_per.get_text(strip=True)
                    product.price_per = remove_str_in_price(price_per)
                prd_image_promo = soup_prd.find('img', class_='img-responsive')
                if prd_image_promo is not None:
                    product.promotion = prd_image_promo.get('src')
                    response = requests.get(product.promotion)
                    bytes_image = Image.open(
                        BytesIO(response.content)).convert('RGB')
                    npimagem = np.asarray(bytes_image).astype(np.uint8)
                    npimagem[:, :, 0] = 0  # zerando o canal R (RED)
                    npimagem[:, :, 2] = 0  # zerando o canal B (BLUE)
                    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)
                    ret, thresh = cv2.threshold(
                        im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    binimagem = Image.fromarray(thresh)
                    phrase = ocr.image_to_string(binimagem)
                    product.promotion = phrase
                    db.write_values(product.name, product.price_of,
                                    product.price_per, product.promotion, datetime.datetime.now(),
                                    datetime.datetime.now())

            print(product.name, product.price_of,
                  product.price_per, product.promotion)

        driver.quit()


# driver.get(q_link.get())
