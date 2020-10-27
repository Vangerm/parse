import requests
from bs4 import BeautifulSoup

url = input("COUB url: ")
r = requests.get(url)

soup = BeautifulSoup(r.text, features="html.parser")
title = soup.find('h3', {'class': 'musicTitle'}).text
author = soup.find('h3', {'class': 'musicAuthor'}).text

print(f'author: {author}'
      f'title: {title}')
