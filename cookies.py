import requests

# Определяем URL сайта
url = 'https://www.auto.ru/'

# Отправляем GET-запрос на сайт
response = requests.get(url)

# Получаем cookies с ответа
cookies = response.cookies

# Выводим полученные cookies
for cookie in cookies:
    print(cookie.name, cookie.value).auto.ru