import os
import csv
from tkinter import PhotoImage
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from requests import get, Response
import telebot
from PIL import ImageTk, Image


load_dotenv()

root = Tk()
root.title('Парсер')
root['bg'] = '#fafafa'
root.wm_attributes('-alpha', 1)

root.resizable(width=False, height=False)

canvas = Canvas(root, width=300, height=250)
image = Image.open("D:\Diplom\log.png")
photo = ImageTk.PhotoImage(image.resize((300, 250)))
image = canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.grid(row=2,column=1)
canvas.pack()

input_label = Label(root, text='Введите данные для парсинга:')
input_label.pack()

entry = Entry(root)
entry.pack()

entry_two = Entry(root)
entry_two.pack()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
PATH = 'Cars.csv'
COOKIE = os.getenv('COOKIE')
HEADERS = {
    'user-agent': os.getenv('USER_AGENT'),
    'accept': os.getenv('ACCEPT'),
    'Accept-Language': 'ru',
    'accept-encoding': 'accept - encoding: gzip, deflate, br',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': COOKIE
}

def get_html(url, headers, params):
    try:
        return get(url, headers=headers, params=params)
    except requests.HTTPError:
        messagebox.showinfo("Message", "При выполнении запроса произошла ошибка")
    
def get_pages_amount(content):
    soup = BeautifulSoup(content, 'html.parser')
    return len(
        soup.find('span',
                  class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination__pages').contents
    )

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ListingItem__description')
    cars = []
    for item in items:
        car = {
            'car': item.find('div', 'ListingItem__summary').get_text(),
            'url': item.find('a', 'Link ListingItemTitle__link').get('href'),
            'price': item.find('div', 'ListingItemPrice__content').get_text().replace(' ', '').replace('₽', ''),
            'year': item.find('div', 'ListingItem__yearBlock').get_text(),
        }
        cars.append(car)
    return cars

def parse(url):
    html = get_html(url, HEADERS,None)
    if html.status_code == 200:
        cars = []
        pages_amount = get_pages_amount(html.content)
        for i in range(1, pages_amount + 1):
            html = get_html(url, HEADERS, params={'page': i})
            cars.extend(get_content(html.content))
        messagebox.showinfo("Message",f'Получены данные по {len(cars)} авто.')
        return sorted(cars, key=lambda car: int(car['year']), reverse=True)
    else:
        messagebox.showinfo("Message",f'При выполнении запроса произошла ошибка')

def save_to_file(data):
    with open(PATH, 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(['Car', 'Link', 'Price (RUR)', 'Year'])
        for car in data:
            w.writerow([
                car['car'],
                car['url'],
                car['price'],
                car['year']
            ])
        file.close()

def send_message(chat_id):
    file = open('Cars.csv', 'rb')
    bot.send_document(chat_id=chat_id, document=file)
    file.close()

def main():
    url = entry.get().strip()
    chat_id = entry_two.get()
    data = parse(url)
    save_to_file(data)
    send_message(chat_id)


button = Button(root, text="Submit", command=main)
button.pack()

root.mainloop()
