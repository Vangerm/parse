import requests

import json
from bs4 import BeautifulSoup

cookies = {
    """ _ab_=%7B%22search-sandbox%22%3A%22default%22%2C%22catalog-hit-filter%22%3A%22filtr_hit_default%22%7D;
    PHPSESSID=e1a9c2a88e5a8306c7f990c93b5c8b53;
    _csrf=f64672e43e125320d851c0e4e53cc66d3b9ed00b527b9bdcbadc92c2adce3c56a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22RT56wXc4V2jeSiXxClZksTqMP0ap5Gy0%22%3B%7D;
    current_path=2833842207c764717eda226cb515bc459f2b17151dd158960f604415a83a10bfa%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A164%3A%22%7B%22city%22%3A%22566ca284-5bea-11e2-aee1-00155d030b1f%22%2C%22cityName%22%3A%22%5Cu0421%5Cu0430%5Cu043d%5Cu043a%5Cu0442-%5Cu041f%5Cu0435%5Cu0442%5Cu0435%5Cu0440%5Cu0431%5Cu0443%5Cu0440%5Cu0433%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D;
    city_path=spb;
    lang=ru;
    qrator_jsid=1695743041.606.lqQNhJGPMcM0Uvhn-oibjhev7shvip8tmjifm6ldof02ckfn7;
    qrator_ssid=1695743042.622.t9TDSW80ChERtO5p-4dba5s044ks8e7gj9l2vjtrcgjg1lk8u;
    ipp_key=v1671272926133/v33947245ba5adc7a72e273/bpybWHDoEOIRlsvtY5Gguw==;
    cartUserCookieIdent_v3=e1d5d4af1b614babe218264844a7f8e5133483a1578de10d084cfa46a8424108a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%2276440ee7-8702-399b-a7b4-a8bb989cc799%22%3B%7D;
    phonesIdent=9ab79f06d67b3c15c59021ff91bbca3432bdfb694a17d113bd441ca9cc805213a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22c2582216-f52a-48ab-b35c-bda4bb91c279%22%3B%7D;
    ipp_uid=1670921834062/t9NBXISnNvquWwjf/7P+lio92Fv6BsB9nwg23Rg==
    """
}

headers = {
    """
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15"
"""
}

urls = {
    "catalog": "/catalog/",
    "videokarty": {
        "url":"https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/",
        "tag":"a",
        "class_":"catalog-product__name ui-link ui-link_black"
    }}

def find_values_from_key(key, json_object):
    """TODO посмотреть, может можно переписать эту лагающую херню)"""
    if isinstance(json_object, list):
        for list_element in json_object:
            yield from find_values_from_key(key, list_element)
    elif isinstance(json_object, dict):
        if key in json_object:
            yield json_object[key]
        for dict_value in json_object.values():
            yield from find_values_from_key(key, dict_value)

def search_Pages(url):
    """
        Поиск количества странниц в категории товара
    """
    response = response_get(url)
    data = json.loads(response.text)
    root = BeautifulSoup(data['html'], 'lxml')

    number_str = []
    parse_namber_str = root.find_all('a', class_='pagination-widget__page-link', href=True)
    if len(parse_namber_str)<1:
        return int(1)
    else:
        for tag in parse_namber_str:
            if tag.get('href')[0] == '/':
                number_str.append(tag.get('href'))
        return int(number_str[-1][-2:])

def response_get(url, params=None):
    """
        Метод запросов GET.
        Возвращает строку с HTML документом.
    """
    response = requests.get(url, cookies=cookies, headers=headers, params=params)

    return response

def price(data_product):
    """"
        Метод парсит цену товара, а точнее, пока что извлекает JSON обьект с содержимым productID
        TODO Требуется Ускорить работу
    """
    """ Как ты и заметил куки и заголовки продублированы в методе PRICE
        Это не случайно. По какой то причине те куки с заголовком, которые отправляются с основным запросом
        не работают. Пришлось отправлять новые... Вероятно вся проблема в csrf токене, а может и нет.
        Не было особо времени заниматься этим. 
    """
    cookiessss = {
        """ Вставляем куки 
        """
    }

    headerssss = {
        """ Вставляем заголовок """
    }

    data_headers = f'data={{"type":"product-buy","containers":' \
                   f'[{{"id":"as-X0HjkI","data":{{"id":"%s"}}}}]}}' % data_product

    params_headers = {
        'cityId': '15', # В данном параметре передается наименование города, в котором ищется товар
        'langId': 'ru',
        'v': '2',
    }

    response = requests.post("https://www.dns-shop.ru/ajax-state/product-buy/",
                            cookies=cookiessss, headers=headerssss, data=data_headers,params=params_headers)

    root = json.loads(response.text)

    return root

def par_videokarty(url):
    """
            Парсер стрницы https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/
    """
    pages = {
        "p": str(search_Pages(url)),
    }

    for page_number in range(1,int(pages["p"])+1):
        response = response_get(url, params={"p":page_number})
        data = json.loads(response.text)
        root = BeautifulSoup(data['html'], 'lxml')
        print('___________________________')
        print('Страница - ', page_number,'\n')
        allSmartfony = root.find_all(urls["videokarty"]["tag"], class_=urls["videokarty"]["class_"])
        art_phone = root.find_all("div", class_="catalog-product ui-button-widget")
        product_id = root.find_all("div", class_="catalog-product ui-button-widget")
        hrefs = root.find_all("a", class_="catalog-product__name ui-link ui-link_black")
        for art, name, data_product, href in zip(art_phone,allSmartfony, product_id,hrefs):
            len_product_name = name.find('span')
            product_art = art.get('data-code')
            data_bd_name = data_product.get('data-product')
            href_links = href.get('href')
            a = list(find_values_from_key("current", price(data_bd_name)))[0]
            b = str(a)
            print('найден товар - ', href_links)
            """ insert_table_smart - Запись в БД артикул, наименование, цену и ссылку товара"""
            # insert_table_smart(product_art,len_product_name.text, b, href_links)

            # TODO Написать более простую функцию фарсинга цены у товара.... Слишком большие задержки
            with open("all_tovar_video.txt", 'a', encoding="utf-8") as f:
                f.write(str(product_art+" - "+len_product_name.text+" - "+b+'\n'))
                f.close()
            print(str(product_art)," - ",len_product_name.text, ' ___ ', b, " Р")
    print('Всего страниц - ', search_Pages(url),'\n')

par_videokarty("https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/")