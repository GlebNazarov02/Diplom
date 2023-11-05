import requests
session = requests.Session()
print(session.cookies.get_dict())
response = session.get('https://auto.ru/moskva/cars/mitsubishi/asx/all/')
print(session.cookies.get_dict())