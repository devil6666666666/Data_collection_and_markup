# Задание: Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

url = "http://books.toscrape.com"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
params = {'page':1}
session = requests.session()

all_posts = []

while True:
    response = session.get(url + "/catalogue", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('article', {'class': 'product_pod'})
    if not posts:
        break

    for post in posts:
        post_info = {}
        name_info = post.find('a',{'class':'title'})
        post_info['name'] = name_info.getText()
        post_info['url'] = url+name_info.get('href')
        post_info['price'] = int(post.find('div',{'class':'product_price'}).getText())
        all_posts.append(post_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

pprint(all_posts)
pprint(len(all_posts))

with open('books_data.json', 'w') as f:
    json.dump(all_posts, f)

