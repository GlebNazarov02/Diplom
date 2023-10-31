import os
import csv
from tkinter import *
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Union
from requests import get, Response
import telebot

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

token = '6359779765:AAH_VH-UsgY4ZdU1FnZHHm1HemOSnPjdpCs'
bot = telebot.TeleBot(token)
PATH = 'Cars.csv'
URL = os.getenv('URL')
COOKIE = os.getenv('COOKIE')
HEADERS = {
    'user-agent': os.getenv('USER_AGENT'),
    'accept': os.getenv('ACCEPT'),
    'Accept-Language': 'ru',
    'accept-encoding': 'accept - encoding: gzip, deflate, br',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': COOKIE
}


def get_pages_amount(content):
    """Calculate number of pages."""
    soup = BeautifulSoup(content, 'html.parser')
    return len(
        soup.find(
            'span',
            class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination__pages'
        ).contents
    )


def get_content(html):
    """Parsing page content."""
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


def get_html(url: str, headers: dict, params: Union[None, dict] = None) -> Response:
    """Getting an answer to the request."""
    try:
        return get(url, headers=headers, params=params)
    except Exception as error:
        raise ConnectionError(f'При выполнении запроса произошла ошибка: {error}')


def parse(url: str):
    """Parsing the request."""
    url = url or URL
    html = get_html(url, HEADERS)
    if html.status_code == 200:
        cars = []
        pages_amount = get_pages_amount(html.content)
        for i in range(1, pages_amount + 1):
            print(f'Парсим {i} страницу из {pages_amount}...')
            html = get_html(url, HEADERS, params={'page': i})
            cars.extend(get_content(html.content))
        print(f'Получены данные по {len(cars)} авто.')
        return sorted(cars, key=lambda car: int(car['year']), reverse=True)
    else:
        print(f'Сайт вернул статус-код {html.status_code}')


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
                car['year']
            ])
        os.startfile(PATH)

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