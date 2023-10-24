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
url = "https://www.citilink.ru/product/smartfon-apple-iphone-13-a2633-128gb-4gb-temn-noch-3g-4g-6-1-1170x2532-1912378/?action=changeCity&space="


def main():
    with open("cities.json") as file:
        all_cities = json.load(file)

    product_info = {}

    for city_name, city_id in all_cities.items():
        req = requests.get(f"{url}{city_id}", headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        product_price = ''
        product_prices = soup.findAll(class_="app-catalog-1f8xctp")
        for i in product_prices:
            product_price = i.get_text()
            break

        product_info[city_name] = product_price

        print(f"Информация по городу {city_name} загружена.")
        sleep(random.randrange(2, 4))

    with open("cities_price_iphone13.json", "w") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)


main()
