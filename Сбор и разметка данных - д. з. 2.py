# Задание: Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, time, timedelta
import time
import re
import json

# Запрос веб-страницы
url = 'https://books.toscrape.com/intl/?ref_=bo_nb_hm_tab'
response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})

# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Вывод ссылок на
release_links = []
for link in soup.find_all('td', ('class', 'a-text-left mojo-field-type-release mojo-cell-wide')):
    release_links.append(link.find('a').get('href'))

# Объединение ссылок с базовым URL-адресом для создания списка URL-адресов
url_joined = []
for link in release_links:
    url_joined.append(urllib.parse.urljoin('https://books.toscrape.com', link))

# Извлечение данных из таблицы построково и сохранение их в списке словарей
data = []
for url in url_joined:
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', {'class': 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
    rows = table.find_all('div', {'class': 'a-section a-spacing-none'})

    row_data = {}
    for row in rows:
        key = row.find('span').text.strip()
        value = row.find_all('span')[1].text.strip()
        if key == 'Opening':
            value = int(re.sub('[^0-9]', '', value))
        elif key == 'Release Date':
            value = value
        elif key == 'Running Time':
            time_delta = datetime.strptime(value, '%H hr %M min') - datetime(1900, 1, 1)
            value = time_delta.total_seconds()
        elif key == 'Genres':
            value = [genre.strip() for genre in value.split('\n') if genre.strip()]
        elif key == 'In Release':
            value = value.replace(' days/3 weeks', '').strip()
        elif key == 'Widest Release':
            value = int(re.sub('[^0-9]', '', value))

        row_data[key] = value

    data.append(row_data)
    time.sleep(10)

# сохранение данных в JSON-файл
with open('books_price_data.json', 'w') as f:
    json.dump(data, f)