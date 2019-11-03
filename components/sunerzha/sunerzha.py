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


def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    #print(response.text)
    return response.text


def csv_writer(data):
    with open('Sunerzha.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['id'],
            data['name'],
            data['category_first'],
            data['category_second'],
            data['price'],
            data['accessibility'],
            data['link'],
            data['pics'],
            data['files'],
            data['feature'],
            data['additional_components'],
            data['extra_option'],
            data['accessories'],
        ))



def connect_to_database(id, name, main_category, undermain_category, price, enable, link, i_pics, i_files, i_feature, i_additional_components, i_extra_option, i_accessories, today_time):
    with open('config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
                                   user=data['user'],
                                   password=data['password'],
                                   host=data['host'],
                                   port=data['port'])
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.SUNERZHA
        (item_id, name, category_first, category_second, price, accessibility, link, pics, files, featurecs, additional_componentscs, extra_option, accessoriescs,parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (id, name, main_category, undermain_category, price, enable, link, i_pics, i_files, i_feature, i_additional_components, i_extra_option, i_accessories,today_time))
        cursor.close()
        connect.close()



'''
        'id': id,                                                     # id
        'name': name,                                                 # Наименование товара
        'category_first': main_category,                              # Категория
        'category_second': undermain_category,                        # Подкатегория
        'price': price,                                               # Цена
        'accessibility': enable,                                      # Наличие на складе
        'link': link,                                                 # Основная ссылка
        'pics': ''.join(list_pics),                                   # Картиночки
        'files': ''.join(list_docs),                                  # Ссылки на документы (скачать)
        'feature': ''.join(list_params),                              # Параметры
        'additional_components': ''.join(list_additional_components), # Доп. комплектующие
        'extra_option': ''.join(list_extra_options),                  # Варианты подключения
        'accessories': ''.join(list_accessories)                      # Аксессуары
'''



first_list = [
    'http://www.sunerzha.com/productions/zrda/products.php?IB=71&IS=2444&IM=R',
    'http://www.sunerzha.com/productions/zrda/products.php?IB=71&IS=2443&IM=R',
    'http://www.sunerzha.com/productions/additional/products.php?IB=21&IS=101&IM=R',
    'http://www.sunerzha.com/productions/additional/products.php?IB=21&IS=102&IM=R',
    'http://www.sunerzha.com/productions/additional/products.php?IB=21&IS=3704&IM=R',
    'http://www.sunerzha.com/productions/classic/products.php?IB=9&IS=113&IM=R'
]
def get_inside_items(html):
    soup = bs(html, 'lxml')
    cards = soup.find('div', class_='all-products-listing').find_all('div', class_='model-card')
    for card in cards:
        print('http://www.sunerzha.com' + card.find('a').get('href'))
        first_list.append('http://www.sunerzha.com' + card.find('a').get('href'))




full_list = []
def get_items(html):
    soup = bs(html, 'lxml')
    cards_newline = soup.find('div', class_='products__listing [ cf ]').find_all('div', class_='products__item product-item onNewLine')
    cards = soup.find('div', class_='products__listing [ cf ]').find_all('div', class_='products__item product-item')
    joinCards = [cards_newline, cards]
    for i in joinCards:
        for card in i:
            card_url = 'http://www.sunerzha.com' + card.find('div', class_='product-item__image').find('a').get('href')
            print(card_url)
            full_list.append(card_url)


def get_dop_items(html):
    soup = bs(html, 'lxml')
    cards_newline = soup.find('div', class_='products__listing-four [ cf ]').find_all('div', class_='products__item-four product-item onNewLine')
    cards = soup.find('div', class_='products__listing-four [ cf ]').find_all('div', class_='products__item-four product-item')
    joinCards = [cards_newline, cards]
    for i in joinCards:
        for card in i:
            card_url = 'http://www.sunerzha.com' + card.find('div', class_='product-item__image').find('a').get('href')
            print(card_url)
            full_list.append(card_url)



def get_data(html):
    soup = bs(html, 'lxml')

    link = soup.find('meta', property='og:url').get('content')
    name = soup.find('h1').text.strip()




    list_pics = []
    pics = soup.find('div', class_='product-detail-photos').find('div', class_='product-detail-photos__more-images [ cf ]').find_all('div')
    for pic in pics:
        try:
            picX = 'http://www.sunerzha.com' + pic.find('a').get('href') + ';; '
            list_pics.append(picX)
        except AttributeError:
            pass

    main_pic = 'http://www.sunerzha.com' + soup.find('div', class_='product-detail-photos').find('div', class_='product-detail-photos__main-image [ cf ]').find('div', class_='product-detail-photos__item').find('a').get('href') + ';; '
    list_pics.append(main_pic)

    list_params = []
    params = soup.find('ul', class_='product-detail-props__table').find_all('li')
    for param in params:
        try:
            feature = param.find('span', class_='productPropDetail').text.replace(' - ','') + ': ' + param.find('span', class_='productPropValue').text + ';; '
            list_params.append(feature)
        except AttributeError:
            pass


    list_docs = []
    docs = soup.find('ul', class_='product-detail-docs__icon').find_all('li')
    for doc in docs:
        if doc.find('a').get('data-filetype') == 'xls':
            pass
        else:
            doc = 'http://www.sunerzha.com' + doc.find('a').get('href') + ';; '
            list_docs.append(doc)


    models = soup.find('table', class_='product-detail-props__models-table').find_all('tr')
    model = models[1]

    id = model.find('td', class_='productPropArticle').text.strip()
    price = model.find('td', class_='productPropPrice').text.strip().replace(' руб.', '')
    try:
        enable = model.find('td', class_='productPropQuantityTrue').text.strip()
    except:
        enable = model.find('td', class_='productPropQuantityFalse').text.strip()



    #print('Варианты подключения')
    # Варианты подключения
    list_extra_options = []
    try:
        extra_option = soup.find('section', class_='product-detail-sets').find_all('div', class_='product-detail-sets-items')
        for extra in extra_option:
            options = extra.find_all('div', class_='product-detail-sets-items__item')
            for option in options:
                option = 'http://www.sunerzha.com' + option.find('a').get('href') + ';; '
                list_extra_options.append(option)
    except:
        pass


    #print('Дополнительные комплектующие')
    # Дополнительные комплектующие
    list_additional_components = []
    try:
        additional_components = soup.find('div', id='linkComplectsBody').find_all('div', class_='product-detail-addons-items__item')
        for component in additional_components:
            component = 'http://www.sunerzha.com' + component.find('a').get('href') + ';; '
            list_additional_components.append(component)
    except:
        pass


    #print('Аксессуары')
    # Аксессуары
    list_accessories = []
    try:
        accessories = soup.find('div', id='linkAcsessoriesBody').find_all('div', class_='product-detail-addons-items__item')
        for acces in accessories:
            acces = 'http://www.sunerzha.com' + acces.find('a').get('href') + ';; '
            list_accessories.append(acces)
    except:
        pass


    # Категория (водяные/электирческие)

    main_category = soup.find('aside', class_='product-nav').find('div', class_='site-menu').find('ul', class_='site-menu__list')\
    .find('li', class_='site-menu__products menuL1open').find('li', class_='menuL2open').find('span', class_='leftMenuSubSelected').text.strip()

    # Подкатегория
    undermain_category = soup.find('aside', class_='product-nav').find('div', class_='site-menu').find('ul', class_='site-menu__list')\
    .find('li', class_='site-menu__products menuL1open').find('li', class_='menuL2open').find('a', class_='leftMenuSubSubSelected').text.strip()


    data = {
        'id': id,                                                     # id
        'name': name,                                                 # Наименование товара
        'category_first': main_category,                              # Категория
        'category_second': undermain_category,                        # Подкатегория
        'price': int(price),                                          # Цена
        'accessibility': enable,                                      # Наличие на складе
        'link': link,                                                 # Основная ссылка
        'pics': ''.join(list_pics),                                   # Картиночки
        'files': ''.join(list_docs),                                  # Ссылки на документы (скачать)
        'feature': ''.join(list_params),                              # Параметры
        'additional_components': ''.join(list_additional_components), # Доп. комплектующие
        'extra_option': ''.join(list_extra_options),                  # Варианты подключения
        'accessories': ''.join(list_accessories)                      # Аксессуары
    }


    i_pics = ''.join(list_pics)
    i_files = ''.join(list_docs)
    i_feature = ''.join(list_params)
    i_additional_components = ''.join(list_additional_components)
    i_extra_option = ''.join(list_extra_options)
    i_accessories = ''.join(list_accessories)
    today_time = str(datetime.date.today())


    print(data)
    #print('----')
    connect_to_database(id, name, main_category, undermain_category, price, enable, link, i_pics, i_files, i_feature,
                        i_additional_components, i_extra_option, i_accessories, today_time)
    #csv_writer(data)




def main():
    headers = h


    FIRST_URLS = ['http://www.sunerzha.com/productions/water/',
                  'http://www.sunerzha.com/productions/electric/',
                  'http://www.sunerzha.com/productions/combined/',
                  ]

    for fURL in FIRST_URLS:
        get_inside_items(get_html(fURL, headers))
        sleep(0.7)


    for fURL1 in first_list:
        try:
            get_items(get_html(fURL1, headers))
        except:
            get_dop_items(get_html(fURL1, headers))
        sleep(0.8)


    for fURL2 in full_list:
        print(fURL2)
        get_data(get_html(fURL2, headers))
        sleep(0.7)
    '''


    urls = [
        'http://www.sunerzha.com/productions/water/infodetail.php?IB=7&IP=636651&IS=2420&IM=R',
        'http://www.sunerzha.com/productions/combined/infodetail.php?IB=78&IP=884948&IS=3725&IM=R',
        'http://www.sunerzha.com/productions/classic/infodetail.php?IB=9&IP=324978&IS=113&IM=R'
    ]
    for u in urls:
        get_data(get_html(u, headers))
    '''

if __name__ == '__main__':
    main()

