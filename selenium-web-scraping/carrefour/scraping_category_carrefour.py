from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
import json
import datetime
from json import JSONEncoder
import csv
import Repository.MySqlRepository.categorydb as db
import mysql.connector

db.delete_values_into_category()
url = 'https://www.carrefour.com.br/dicas/mercado?crfint=hm|header-menu|mercado|9'
base_url = 'https://www.carrefour.com.br'

class Category():
    def __init__(self, name, link):
        self.name = name
        self.link = link

class CategoryEndoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

f = csv.writer(open('categories.csv', 'w'))
f.writerow(['Name', 'Link', 'Created', 'Updated'])

option = webdriver.ChromeOptions()
option.add_argument(' — incognito')
driver = webdriver.Chrome(executable_path=r'C:\Python\chromedriver.exe', options=option)

driver.get(url)

timeout = 60
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,'mercado-menu__ul')))
except TimeoutException:
    print('Timed out waiting for page to load')
    driver.quit()

html_content = driver.find_element_by_class_name('mercado-menu__wrapper')
market_categories_into_menu = html_content.get_attribute('innerHTML')
soup = BeautifulSoup(market_categories_into_menu, 'html.parser')
category_name_list_items = soup.find_all('a')

for categories in category_name_list_items:
    category_name = categories.find('span')
    name = (category_name.contents[0])
    if(name == 'Matinais'):
        links = categories.get('href')
    else:    
        links = (base_url + categories.get('href'))
    category = Category(name, links)
    f.writerow([" ".join(category.name.split()), category.link, datetime.datetime.now(), datetime.datetime.now()])
    db.write_values(" ".join(category.name.split()), category.link, datetime.datetime.now(), datetime.datetime.now())
driver.quit()   
