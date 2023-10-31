import os
import csv
import telebot
import os
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Union
from requests import get, Response
import time

url = 'https://anti-captcha.com/api/solve'
browser = webdriver.Chrome()
browser.get('https://auto.ru/moskva/cars/kia/k3/all/')
time.sleep(5)
soup = BeautifulSoup(browser.page_source, 'html.parser')