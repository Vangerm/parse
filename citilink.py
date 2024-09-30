import random
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
import functools


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15"
}


def load_check(func):
    @functools.wraps(func)
    def wrapper(category_name, category_href, count):
        print(f'Начинаю выгружать {category_name}')
        return func(category_name, category_href, count)
    return wrapper


def soup_web(url):
    req = requests.get(url, headers=headers)
    src = req.text

    # with open("index.html", 'w', encoding='utf-8') as file:
    #     file.write(src)
    #
    # Достаем заголовки и ссылки на каталоги
    #
    # with open("index.html") as file:
    #     src = file.read()

    # Обрабатываем супом и выгружаем список тегов "а" с классом начинающимся с "Category_subTitle"
    return BeautifulSoup(src, "lxml")


def open_json_file():
    with open("citilink/all_categories_dict.json", encoding='utf-8') as file:
        return json.load(file)


def products(soup, category_name: str):

    """Функция предназначеная для вытаскивания товаров со страницы

    Args:
        soup (bs4): страница с товарами
        category_name (str): категория выгрузки
    """

    # нахождение всех наименований товаров на страницы и их цен
    product_title = soup.find_all("a", class_=re.compile("CardText_link"))
    product_price = soup.find_all(class_=re.compile("CardPrice_bottom"))

    product_info = []

    # перебор и выгрузка в данных в файлы csv и json
    for item in range(len(product_title)):
        with open(f"citilink/{category_name}.csv", "a", encoding="utf-8", newline='') as file:
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

    # выгрузка конечного списка товаров в json файл
    with open(f"citilink/{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)


# @load_check - декоратор срабатывает, но функция нет, проверить!!!!
def discharge_category(category_name: str, category_href: str):

    """Функция выгружает товары одной категории в файлы csv и json

    Args:
        category_name (str): Наименование категории
        category_href (str): Ссылка на категорию
    """

    # Чистка наименований категорий от всякого мусора
    # rep = [",", " ", "-", "/"]
    # for item in rep:
    #     if item in category_name:
    #         category_name = category_name.replace(item, "_")

    soup = soup_web(url=category_href)

    # Вписываем заголовки в таблицу
    with open(f"citilink/{category_name}.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Название",
                "Стоимость",
                "Ссылка"
            )
        )

    products(soup=soup, category_name=category_name)

    # Вытаскиваем страницы и находим максимальную
    pages = soup.find_all("a", class_=re.compile("PaginationBody_item__link"))
    pages = int(pages[-1].text)

    # перебираем страницы и дописываем товары
    for page in range(2, pages + 1):
        products(soup=soup_web(url=category_href + f"?page={page}"), category_name=category_name)

    # print(f"Выгрузка раздела - {category_name}, завершена.") - занести в деккоратор
    sleep(random.randrange(2, 4))


def discharge_categories(categories_name=()):
    """Функция для выгрузки ссылок из каталога на определенные категории

    Args:
        categories_name (set): список категорий, которые необходимы для дальнейшей выгрузки
    """
    # Достаем главную страницу
    url = (
        "https://www.citilink.ru/catalog/komplektuyuschie-dlya-pk/",
        "https://www.citilink.ru/catalog/zhestkie-diski-i-ssd/"
        )

    # Словарь для хранения категорий с сайта
    all_categories_dict = {}

    # Делаем запросы на страницы и выгружаем в переменную
    for soup in url:

        all_products_href = soup_web(url=soup).find_all(name='a', class_=re.compile("app-catalog"))

        # Перебор списка тегов, вытаскиваем наименование раздела и добавляем в словарь каталогов
        for item in all_products_href:
            item_text = item.text.lower()
            item_href = "https://www.citilink.ru" + item.get("href")

            # Временное ограничение на комплектующие для сборки пк
            if item_text in categories_name:
                all_categories_dict[item_text] = item_href

    # Выгружаем список в json файл
    with open("citilink/all_categories_dict.json", "w", encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


def load_categories():
    # Открываем сформированный список категорий
    all_categories = open_json_file()

    # Проходим по по всем категориям и записываем их в основную папку
    for category_name, category_href in all_categories.items():
        discharge_category(category_name=category_name, category_href=category_href)


categories_name = (
    'процессоры',
    'материнские платы',
    'видеокарты',
    'оперативная память',
    'блоки питания',
    'корпуса',
    'жёсткие диски',
    'накопители ssd',
    'системы охлаждения',
    'системы охлаждения процессора',
    'ssd накопители'
    )
discharge_categories(categories_name)
