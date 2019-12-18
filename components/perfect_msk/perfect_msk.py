#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import csv
from pprint import pprint
from config import headers as h
from time import sleep
import psycopg2
import datetime
import json
import re
from kafka import KafkaProducer, KafkaConsumer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))



def csv_writer(data):
    with open('/home/arty/python/adhoc_parser/components/perfect_msk/perfect_msk.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['name'],
            data['articul'],
            data['category1'],
            data['category2'],
            data['feature'],
            data['description'],
            data['produce'],
            data['price'],
            data['picture'],
            data['recomended'],
            data['complect'],
            data['link']
        ))



def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    # print(response.text)
    return response.text


def get_catalog(html):
    list_catalog = []
    soup = bs(html, 'lxml')
    catalogs = soup.find('div', class_='module catalog').find('div', class_='catalog-list clearfix')\
    .find_all('div', class_='catalog-list__item')
    for catalog in catalogs:
        catalog = catalog.find('a').get('href')
        list_catalog.append(catalog)
    return list_catalog

WITHJS = []
def get_underCatalog(html):
    soup = bs(html, 'lxml')
    try:
        under_catalogs = soup.find('div', class_='zameniMenyaNaFiltrovannoe')\
        .find('div', class_='clisting catalog-list clearfix')\
        .find_all('div', class_='catalog-list__item')
        for catalog in under_catalogs:
            catalogx = catalog.find('a').get('href')
            WITHJS.append(catalogx)
    except AttributeError as e:
        print(e)
        pass


around_js = []
def around_java_script(html):
    soup = bs(html, 'lxml')
    try:
        links = soup.find('div', class_='glide__wrapper').find('ul', class_='glide__track')\
        .find('li', class_='glide__slide')\
        .find_all('div')
        print(type(links))

        for link in links:
            try:
                linkx = link.find('div', class_='product_photo').find('a').get('href')
                around_js.append(linkx)
                print('Around JS link is: ' + linkx)
            except:
                pass
    except:
        pass


bonus_orders = []
def get_data(urlx, html):
    soup = bs(html, 'lxml')
    name = soup.find('h2', class_='product-header__title').text.strip()
    # print(name)
    try:
        articul = soup.find('div', class_='product-header').find('div', class_='art').text.strip()
        # print(articul)
    except:
        articul = None
    category1 = soup.find('div', id='breadcrumbs').find_all('a')[0].text.strip()
    try:
        category2 = soup.find('div', id='breadcrumbs').find_all('a')[1].text.strip()
    except:
        category2 = ''
    # print(category1)
    # print(category2)

    list_features = []
    features = soup.find('div', class_='dop_atr').find_all('div', class_='prod_dop_option')
    for feature in features:
        feature = feature.text.strip()
        list_features.append(feature)
        # print(feature)
    try:
        description = soup.find('div', class_='product-desc').find('p').text.strip()
    except:
        description = ''
    # print(description)
    produce = soup.find('div', class_='prod_dop_option').text.strip()
    # print(produce)
    try:
        price = soup.find('div', class_='product-prod_prices').find('span', class_='price').text.strip().replace(' ', '')
    except:
        price = None
    # print(price)
    picture = soup.find('div', class_='product_photo').find('a').find('img').get('src')
    # print(picture)
    try:
        recomended = soup.find('div', class_='product_recc_prod').find('div', class_='item-list owl-carusel clearfix')\
        .find_all('div')
        list_recomended = []
        for recm in recomended:
            try:
                recm = recm.find('div', class_='product_photo').find('a').get('href')
                list_recomended.append(recm)
                bonus_orders.append(recm)
                # print(recm)
            except:
                pass
    except:
        list_recomended = ''
    try:
        complect = soup.find('div', class_='fullcomplect_block').find('div', class_='prd_items')\
        .find('div').find('div', class_='info').find('a').find('b').text.strip() + ': ' + 'http://perfect-msk.ru' + soup.find('div', class_='fullcomplect_block').find('div', class_='prd_items')\
        .find('div').find('div', class_='info').find('a').get('href')
    except:
        complect = ''


    today_time = str(datetime.date.today())

    data = {
        'name': name,
        'articul': articul,
        'category1': category1,
        'category2': category2,
        'feature': ' ;; '.join(list_features),
        'description': description,
        'produce': produce,
        'price': price,
        'picture': picture,
        'recomended': ' ;; '.join(list_recomended),
        'complect': complect,
        'link': urlx,
        'parse_date': today_time
    }
    print(data)
    producer.send('perfect_msk', key=b'row_perfect', value=data)

    #csv_writer(data)



def main():
    headers = h
    main_url = 'http://perfect-msk.ru/'

    # first_catalog = get_catalog(get_html(main_url, headers))
    # for url in first_catalog:
    #     print('url: ' + url)
    #     get_underCatalog(get_html(url, headers))
    #
    # for under in WITHJS:
    #     print(under)
    #     around_java_script(get_html(under, headers))
    #     sleep(0.4)
    # print(len(around_js))
    #
    # for x in around_js:
    #     print('now go to parse this url: ' + x)
    #     get_data(x, get_html(x, headers))
    #     sleep(0.3)
    #
    # print('len after: ' + str(len(bonus_orders)))
    # print('len before: ' + str(len(set(bonus_orders))))
    #
    # for y in set(bonus_orders):
    #     print('now go to parse this url: ' + y)
    #     get_data(y, get_html(y, headers))
    #     sleep(0.3)





    urls = ['http://perfect-msk.ru/ishop/product/793',
    'http://perfect-msk.ru/ishop/product/811',
    'http://perfect-msk.ru/ishop/product/1568',
    'http://perfect-msk.ru/ishop/product/1638',
    'http://perfect-msk.ru/%D0%BA%D0%BB%D0%B5%D0%B9%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B0%D0%B6%D0%BD%D1%8B%D0%B9',
    'http://perfect-msk.ru/ishop/product/113',
    'http://perfect-msk.ru/ishop/product/992']
    for url in urls:
        get_data(url, get_html(url, headers))
        sleep(0.6)
        print('--------------------------')


if __name__ == '__main__':
    main()
