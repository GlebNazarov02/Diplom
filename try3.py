import os
import csv
import telebot
import os
from tkinter import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import csv
import time



root = Tk()
root.title('Парсер')
root['bg'] = '#fafafa'
root.wm_attributes('-alpha', 0.7)

root.resizable(width=False, height=False)

canvas = Canvas(root, width=300, height=250)
canvas.pack()

frame = Frame(root, bg='red')
frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)

input_label = Label(root, text='Введите данные для парсинга:')
input_label.pack()

entry = Entry(root)
entry.pack()

entry_two = Entry(root)
entry_two.pack()

PATH = 'Cars.csv'

cars=[]
pages = []
token = '6359779765:AAH_VH-UsgY4ZdU1FnZHHm1HemOSnPjdpCs'
bot = telebot.TeleBot(token)


def getpagecontent(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(15)
    try:
        popup_element = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//span[@class="Link PromoPopupHistory__body-link"]')))
    except:
        popup_element = None

    if(popup_element != None):
        button_promo = browser.find_element(By.XPATH, '//span[@class="Link PromoPopupHistory__body-link"]')
        button_promo.click()

    block = browser.find_elements(By.CLASS_NAME,'ListingItem__description')
    if not pages:
        try:
            pagesblock = browser.find_elements(By.CLASS_NAME,'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination__page')
        except:
            pass
        for a in pagesblock:
            pages.append(a.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    return block


def writecars(block):
    for car in block:
        car = {
            'car': car.find_element(By.CLASS_NAME, 'ListingItem__summary').text,
            'url': car.find_element(By.TAG_NAME, 'a').get_attribute('href'),
            'price': car.find_element(By.CLASS_NAME,  'ListingItem__priceBlock').text.replace('РѕС‚ ',''),
            'year': car.find_element(By.CLASS_NAME,  'ListingItem__yearBlock').text
        }
        cars.append(car)
    return cars


def save_to_file(data) -> None:
    """Saving data to file."""
    with open(PATH, 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(['Car', 'Link', 'Price (RUR)', 'Year'])
        for car in data:
            w.writerow([
                car['car'],
                car['url'],
                car['price'],
                car['year'],
            ])
        os.startfile(PATH)


def send_message(chat_id):
    file = open('Cars.csv', 'rb')
    bot.send_document(chat_id=chat_id, document=file)
    file.close()



def main():
    url = entry.get().strip()
    chat_id = entry_two.get()
    block = getpagecontent(url)
    writecars(block)
    for page in pages:
        block = getpagecontent(page)
        writecars(block)
        save_to_file(cars)
        send_message(chat_id)


button = Button(root, text="Submit", command=main)
button.pack()

root.mainloop()
