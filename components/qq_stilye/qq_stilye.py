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


def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    #print(response.text)
    return response.text

list_cards = []
def get_cards(html):
    soup = bs(html, 'lxml')
    cards = soup.find('div', id='products')
    for card in cards:
        try:
            card = 'https://qq.ru' + card.find('div').find_all('a')[2].get('href')
            list_cards.append(card)
            #card = card.find('div').find_all('a')[1].get('href')
            print(str(card) + '\n----------------')
        except AttributeError:
            pass


def get_maxpage(html):
    soup = bs(html, 'lxml')
    page = soup.find('div', class_='pagination_flex').find('div', class_='pagination__pages pages').find_all('a')[-1].text.strip()
    return int(page)



def get_data(html):
    soup = bs(html, 'lxml')
    articul = soup.find('div', class_='product-detail-info__text')\
    .find('div', id='js_product_detail_info').find('fieldset', class_='product-detail-config__artikul artikul')\
    .find('span').text.strip()

    enable = soup.find('div', class_='product-detail-info__text')\
    .find('div', id='js_product_detail_info').find('div', class_='product-detail-config__amount').text.strip()
    if enable == '':
        enable = 'Нет в наличии'

    code = soup.find('div', class_='product-detail-info__text')\
    .find('div', id='js_product_detail_info').find('fieldset', class_='product-detail-config__code code')\
    .find('span').text.strip()

    price = soup.find('div', class_='product-detail-info__text')\
    .find('div', id='js_product_detail_info').find('div', class_='product-detail-config__item-price')\
    .find('span').text.strip().replace(' ', '')


    name = soup.find('div', id='product_detail').find('h1').text.strip()

    link = soup.find('link', rel='canonical').get('href')

    main_pic = 'https://qq.ru' + soup.find('div', id='preview').find('a').get('href')


    list_other_pic = []
    try:
        other_pic = soup.find('div', class_='product-detail-gallery__thumbs').find('ul').find_all('li')
        for pic in other_pic:
            pic = 'https://qq.ru' + pic.find('a').get('href') + ' ;; '
            list_other_pic.append(pic)
    except AttributeError:
        pic = ''
        list_other_pic.append(pic)

    ready_other_pic = ''.join(list_other_pic)


    paths = soup.find('ol', class_='breadcrumbs-list').find_all('li')[2:]
    list_path = []
    for path in paths:
        path = path.text.strip() + '/'
        list_path.append(path)
    ready_path = ''.join(list_path)


    list_features = []
    features = soup.find('div', class_='product-detail-specs__content has-collapse__body')\
    .find('table', class_='prodProps').find_all('tr')
    for td in features:
        td = td.text.strip().replace('\n', '') + ' ;; '
        list_features.append(td)
    ready_features = ''.join(list_features)

    try:
        description_complect = soup.find('div', class_='product-detail-description__content has-collapse__body')\
        .text.strip().replace('\n', ' ;; ')
    except AttributeError:
        description_complect = None

    data = {
        'articul': articul,
        'enable': enable,
        'code': code,
        'price': price,
        'name': name,
        'link': link,
        'main_pic': main_pic,
        'other_pic': ready_other_pic,
        'path': ready_path,
        'features': ready_features,
        'description': description_complect,
    }
    print(data)


def main():
    headers = h
    xurl = 'https://qq.ru/category/00000029104/?q=1K&page='
    #get_cards(get_html(url, headers))
    maxpage = get_maxpage(get_html(xurl, headers))

    # Собираем список карточек, пробегая по всем страницам в ссылке в list_cards
    for page in range(1, maxpage + 1):
        url = xurl + str(page)
        get_cards(get_html(url, headers))
        sleep(0.6)

    for url in list_cards:
        print(url)
        get_data(get_html(url, headers))
        sleep(0.9)

    '''
    urls = [
        'https://qq.ru/product/00000126187/',
        'https://qq.ru/product/00000013454/',
        'https://qq.ru/product/00000126187/',
        'https://qq.ru/product/00000126121/',
        'https://qq.ru/product/00000091678/',
        'https://qq.ru/product/00000126102/'
    ]
    for url in urls:
        get_data(get_html(url, headers))
    '''

if __name__ == '__main__':
    main()