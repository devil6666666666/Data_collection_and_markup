# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название, адрес и рейтинг каждого заведения в консоль.

import requests
import json

# Ваши учетные данные API
#API_Key = fsq3vZGqX83sRJ0Izv2hMWihj+/+0mGGX6qvsbYbmuC+geI=
client_id = "5IFYAN0GRNE0BQ2BZDDZ5AIZGTWEKOCDAKJ3H2DJWNCODOAW"
client_secret = "XBGLLSQXLRFBNTUQILEPLVJGOOCBFGUWJDVW20QIXUFSS3NG"

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")
category = input("Введите интересующую категорию: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": category
}
access_token = "DU23TITYGWEDXKVPSC4WCOQ21L3J34GBQNE4JVGVCZHQ4A1B"
headers = {
    "Accept": "application/json",
    "Authorization": access_token
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)