#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import csv
from help_urls import headers as h
from help_urls import GROHE_URLS
import pprint
from time import sleep
import datetime
import psycopg2
import json


def csv_writer(data):
    with open('ShopGrohe.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['id'],
            data['name'],
            data['category'],
            data['price'],
            data['info'],
            data['download'],
            data['pictures'],
            data['link'],
        ))
        '''
        'id': id,
        'name': name,
        'category': category,
        'price': price,
        'info': information,
        'download': tab_download,
        'pictures': ''.join(list_pictures)
        '''

def connect_to_database(id, name, category, pricex, db_info, tab_download, db_pictures, link, today_time):
    #with open('config.json', 'r') as file1:
    with open('/home/ubpc/adhoc_parser_database/components/grohe/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
                                   user=data['user'],
                                   password=data['password'],
                                   host=data['host'],
                                   port=data['port'])
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.grohe
        (articul, name, category, price, info, downloads, pictures, link, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (id, name, category, pricex, db_info, tab_download, db_pictures, link, today_time))
        cursor.close()
        connect.close()


'''
        'id': id,
        'name': name,
        'category': category,
        'price': int(price.replace('\xa0', '')),
        'info': ''.join(information),
        'download': tab_download,
        'pictures': ''.join(list_pictures),
        'link': link
'''





def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    #print(response.text)
    return response.text


list_cards = []
def get_catalog(html):
    soup = bs(html, 'lxml')
    cards = soup.find('div', class_='tab-content clear-style category-products').find_all('div', class_='masonry-grid-item ph-0')
    for card in cards:
        card = card.find('div', class_='overlay-container').find('a').get('href')
        print(card)
        list_cards.append(card)



def get_data(html):
    soup = bs(html, 'lxml')
    try:
        id = soup.find('div', class_='product-info__top-right').find('div', class_='product-info__sku sku__container').text.replace('\n', '').strip()
    except:
        id = 'Null'
    try:
        category = soup.find('ol', class_='breadcrumb').find_all('li')[2].text.strip()
    except:
        category = 'Null'

    try:
        name = soup.find('div', id='product-info').find('div', class_='product-info__description-name').text
    except:
        name = 'Null'

    try:
        price = (soup.find('div', id='product-info').find('div', class_='product-price__block-info').find('span', class_='productproduct-price__price')\
            .text.replace(' ₽Купить', '').replace(' ₽', '').replace(' ', '').strip())
    except:
        try:
            price = (soup.find('div', id='product-info').find('div', class_='product-price__block-info').find('span',class_='product-price__special') \
                        .text.replace(' ₽Купить', '').replace(' ₽', '').replace(' ', '').strip() + ' ' + soup.find('div',id='product-info').find('div',class_='product-price__block-info').find('span', class_='savings').find('span', class_='savings__procent').text.replace(' ', '').strip())
        except:
            price = ''
    information = []

    try:
        tab_additional = soup.find('div', class_='product-collateral').find('div', id='tab-additional').find_all('div', class_='attribute-set')
        l1 = []
        l2 = []
        for tab in tab_additional:
            keys = tab.find_all('dt')
            for key in keys:
                key = key.text
                l1.append(key)
            values = tab.find_all('dd')
            for value in values:
                value = value.text
                l2.append(value)
        index = -1
        for n in range(len(l1)):
            index = index + 1
            dict = l1[index].replace('\n', '') + ' ' +  l2[index].replace('\n', '') + ', '
            information.append(dict)
    except:
        information.append('Нет вкладки Характеристики')


    try:
        tab_downloads = soup.find('div', id='tab-downloads').find_all('td', class_='doc-icon')
        for tab_download in tab_downloads:
            tab_download = tab_download.find('img').get('src')
    except:
        tab_download = 'Null'

    list_pictures = []
    try:
        pictures = soup.find('div', class_='right-info').find('div', class_='swiper-slider').find_all('div', class_='swiper-slide')
        for pic in pictures:
            try:
                pic = pic.find('a').get('href') + ', '
            except:
                pic = pic.find('img').get('src') + ', '
            list_pictures.append(pic)

    except:
        pic = 'Not picture'
        list_pictures.append(pic)

    link = soup.find('link', rel='canonical').get('href')
    #print(link)

    pricex = price.replace('\xa0', '')
    data = {
        'id': id,
        'name': name,
        'category': category,
        'price': pricex,
        'info': ''.join(information),
        'download': tab_download,
        'pictures': ''.join(list_pictures),
        'link': link
    }

    db_info = ''.join(information)
    db_pictures = ''.join(list_pictures)
    today_time = str(datetime.date.today())

    print(data)
    connect_to_database(id, name, category, pricex, db_info, tab_download, db_pictures, link, today_time)
    #csv_writer(data)



def main():
    headers = h
    '''

    urls = ['https://shop.grohe.ru/vannaya/smesiteli-dlja-vannoj-s-termostatom/termostat-dlja-vanny-grohe-grohtherm-1000-new-hrom.html',
            'https://shop.grohe.ru/vannaya/smesiteli-dlja-rakoviny/smesitel-odnorychazhnyy-grohe-wave-dlya-rakoviny-s-size-hrom-23581001.html',
            'https://shop.grohe.ru/vannaya/smesiteli-dlja-rakoviny/smesitel-dlja-rakoviny-grohe-euroeco-new-hrom.html',
            'https://shop.grohe.ru/vannaya/smesiteli-dlja-rakoviny/infrakrasnyj-smesitel-dlja-rakoviny-grohe-eurosmart-cosmopolitan-e-hrom.html',
            'https://shop.grohe.ru/wc/paneli-smiva/panel-smyva-dlja-unitaza-grohe-skate-cosmopolitan-3-rezhima-smyva-hrom.html']
    for url in urls:
        get_data(get_html(url, h))
        sleep(1)

    '''
    # test to integer
    for url in GROHE_URLS:
        get_catalog(get_html(url + '?limit=all', headers))
        sleep(1)

    print('Len list Urls is: ' + str(len(list_cards)))


    #https://shop.grohe.ru/vannaya/smesiteli-dlja-rakoviny
    #get_catalog(get_html('https://shop.grohe.ru/vannaya/smesiteli-dlja-rakoviny', headers))

    for u in list_cards:
        print(u)
        get_data(get_html(u, h))
        sleep(1)

if __name__ == '__main__':
    main()

#'price': '8\xa0050\xa0₽ 6\xa0450\xa0₽-20% Экономия 1\xa0600'