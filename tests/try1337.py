from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os
import csv
import time

PATH = 'Cars.csv'

cars=[]
pages = []

   
def getpagecontent(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(300)
    block = browser.find_elements(By.CLASS_NAME,'ListingItem__description')
    if not pages:
        pagesblock = browser.find_elements(By.CLASS_NAME,'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination__page')
        for a in pagesblock:
            pages.append(a.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    return block


def writecars(block):
    global cars
    for car in block:
        car = {
            'car': car.find_element(By.CLASS_NAME, 'ListingItem__summary').text,
            'url': car.find_element(By.TAG_NAME, 'a').get_attribute('href'),
            'price': car.find_element(By.CLASS_NAME,  'ListingItem__priceBlock').text.replace('РѕС‚ ',''),
            'year': car.find_element(By.CLASS_NAME,  'ListingItem__yearBlock').text
        }
        cars.append(car)
    return cars


url = "https://auto.ru/moskva/cars/all/?catalog_filter=mark%3DAUDI%2Cmodel%3DA5%2Cgeneration%3D21745628&catalog_filter=mark%3DAUDI%2Cmodel%3DA5%2Cgeneration%3D20795592&sort=fresh_relevance_1-desc"
block = getpagecontent(url)
writecars(block)
for page in pages:
    block = getpagecontent(page)
    writecars(block)
with open(PATH, 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(['Car', 'Link', 'Price (RUR)', 'Year'])
        for car in cars:
            w.writerow([
                car['car'],
                car['url'],
                car['price'],
                car['year'],
            ])
        os.startfile(PATH)
