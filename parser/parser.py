import random
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
import json
import csv


class Parser:
    _ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    _HEADERS = [
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; Pixel 3)"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0)"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Linux; Ubuntu; X11; rv:92.0) Gecko/20100101 Firefox/92.0"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0"
        },
        {
            "Accept": _ACCEPT,
            "User-Agent": "Opera/68.0.3618.173 (Windows NT 10.0; Win64; x64) Presto/2.12.388 Version/12.16"
        }]

    @staticmethod
    def _url_to_list(urls: list[str] | str) -> list[str]:
        """Метод преобразования url адреса в список, если передан список
        он и возвращается, в ином случае возвращается пустой список

        Args:
            urls (list[str] | str): ожидается список из строк или строка

        Returns:
            list[str]: возвращает список строк
        """
        if isinstance(urls, str):
            return [urls]
        elif isinstance(urls, list):
            result = list()
            for url in urls:
                if isinstance(url, str):
                    result.append(url)
            return result
        return []

    @staticmethod
    def _main_web_url(url) -> None | str:
        """Метод достает ссылку на главную страницу ресурса

        Args:
            url (str): ссылка на ресурс

        Returns:
            None | str: ссылка на главную страницу ресурса
        """
        url = re.search(r'.*?\.ru', url)
        if url:
            url = url.group(0)
        return url

    @classmethod
    def _soup_web(cls, url: str) -> BeautifulSoup:
        """Метод делающий запрос полученную ссылку и возвращающий ее страницу

        Args:
            url (str): ссылка на ресурс

        Returns:
            BeautifulSoup: html страница сайта
        """
        req = requests.get(url, headers=random.choice(cls._HEADERS))
        src = req.text

        return BeautifulSoup(src, "lxml")

    def discharge_categories(
            self, urls: list[str] | str,
            class_serch: str,
            tag: str = 'a',
            categories_name: list[str] | str = []
            ) -> None:
        """Метод для выгрузки ссылок из каталога на все
        или определенные категории

        Args:
            urls (list[str] | str): список строк или строка ссылок
            class_serch (str): наименование или часть наименования класса
            tag (str, optional): Тег поиска. Defaults to 'a'.
            categories_name (list[str] | str, optional): список строк или строка определенных категорий. Defaults to [].

        Raises:
            ValueError: Вызывается в случае не переданных ссылок/ки
        """

        self.urls = self._url_to_list(urls)
        if len(self.urls) < 1:
            raise ValueError("Ссылка/ки не найдены")
        self.main_url = self._main_web_url(self.urls[0])

        # Словарь для хранения категорий с сайта
        self.all_categories_dict: dict = dict()

        # Делаем запросы на страницы и выгружаем в переменную
        for url in self.urls:
            all_products_href = self._soup_web(url=url).find_all(
                name=tag,
                class_=re.compile(class_serch)
                )

            sleep(random.randrange(1, 3))

            for item in all_products_href:
                item_text = item.text.lower()

                if categories_name:
                    if item_text in categories_name:
                        item_href = self.main_url + item.get("href")
                        self.all_categories_dict[item_text] = item_href
                else:
                    item_href = self.main_url + item.get("href")
                    self.all_categories_dict[item_text] = item_href

        # Выгружаем список в json файл
        with open(
            f"categories/{self.main_url[12:]}_categories_dict.json",
                "w",
                encoding="utf-8") as file:
            json.dump(
                self.all_categories_dict,
                file,
                indent=4,
                ensure_ascii=False)
