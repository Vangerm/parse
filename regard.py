import random
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
import lxml


headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15"
    }

def products(soup, count, category_name):

    # Находим нужные поля и заполняем таблицу
    product_title = soup.find_all("a", class_=re.compile("CardText_link"))
    product_price = soup.find_all(class_=re.compile("CardPrice_bottom"))

    product_info = []

    for item in range(len(product_title)):
        with open(f"regard/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            href = "https://www.regard.ru" + product_title[item].get("href")
            writer = csv.writer(file)
            writer.writerow(
                (
                    product_title[item].text,
                    product_price[item].text,
                    href
                )
            )

            product_info.append(
                {
                    "Title": product_title[item].text,
                    "Price": product_price[item].text,
                    "Href": href
                }
            )

    with open(f"regard/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

def main():
    # Достаем главную страницу
    url = "https://www.regard.ru"

    req = requests.get(url, headers=headers)
    src = req.text

    # with open("index.html", 'w') as file:
    #     file.write(src)

    # Достаем заголовки и ссылки на каталоги
    #
    # with open("index.html") as file:
    #     src = file.read()
    #
    soup = BeautifulSoup(src, "lxml")
    all_products_href =  soup.find_all(class_=re.compile("Category_subTitle"))

    all_categories_dict = {}

    for item in all_products_href:
        item_text = item.text
        item_href = "https://www.regard.ru" + item.get("href")

        all_categories_dict[item_text] = item_href

    with open("regard/all_categories_dict.json", "w") as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    with open("regard/all_categories_dict.json") as file:
        all_categories = json.load(file)

    count = 0
    for category_name, category_href in all_categories.items():
        rep = [",", " ", "-", "/"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

        print(f"Начинаю выгрузку раздела: {category_name}...")

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        # with open(f"regard/{count}_{category_name}.html", "w") as file:
        #     file.write(src)

        # with open(f"regard/{count}_{category_name}.html") as file:
        #     src = file.read()

        soup = BeautifulSoup(src, "lxml")

        # Вписываем заголовки в таблицу
        with open(f"regard/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    "Название",
                    "Стоимость",
                    "Ссылка"
                )
            )

        products(soup=soup, count=count, category_name=category_name)

        # Вытаскиваем страницы
        pages = soup.find_all("a", class_="Pagination_item__link__vQTps")
        pages = int(pages[len(pages) - 1].text)

        for page in range(2, pages+1):
            req = requests.get(url=category_href + f"?page={page}", headers=headers)
            src = req.text

            soup = BeautifulSoup(src, "lxml")
            products(soup=soup, count=count, category_name=category_name)

        print(f"Выгрузка раздела - {category_name}, завершена.")
        sleep(random.randrange(2, 4))

        count += 1


main()
