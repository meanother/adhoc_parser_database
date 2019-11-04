#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import csv
from pprint import pprint
from config import headers as h
from time import sleep
import datetime
import psycopg2
import json

'''
        'id': id,                                       # id
        'link': link,                                   # Линк
        'name': name,                                   # Наименование
        'description': description,                     # Описание
        'link_material': link_material,                 # Линк на материал (где банка с краской)
        'name_material': name_material,                 # Имя этого материала
        'price': price,                                 # Цена руб/м2
        'complexity': complexity,                       # Сложность нанесения
        'price_for_work': price_for_work,               # Цена за работу руб/м2
        'colors': ''.join(FINAL_picture_list),          # Ссылки вкладки COLORS
        'main_pic': main_pic,                           # Основная картинка (Большая)
        'default_pic': default_pic,                     # Дефолтная картинка (Слева от описания, цен и тд)
        'system': ''.join(tab_system)                   # Вкладка SYSTEM в виде: n1>name;; n2;; n3;; n4;; | - конец табличной строки
'''
def csv_writer(data):
    with open('Pratta.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['id'],
            data['link'],
            data['name'],
            data['description'],
            data['link_material'],
            data['name_material'],
            data['price'],
            data['complexity'],
            data['price_for_work'],
            data['colors'],
            data['main_pic'],
            data['default_pic'],
            data['system'],
        ))

'''
    id      serial       not null
        constraint pratta_key primary key,
    articul varchar(255) not null,
    link    text         null,
    name varchar(255) not null ,
    description text null,
    link_material text null ,
    name_material text null,
    price int null ,
    complexity varchar(255) null ,
    price_for_work int null ,
    colors text null,
    main_pic text null ,
    default_pic text null ,
    systems text null ,
    parse_date date);
'''

def connect_to_database(id, link, name, description, link_material, name_material, price, complexity, price_for_work, db_colors, main_pic, default_pic, db_system, today_time):
    #with open('config.json', 'r') as file1:
    with open('/home/ubpc/adhoc_parser_database/components/pratta/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
                                   user=data['user'],
                                   password=data['password'],
                                   host=data['host'],
                                   port=data['port'])
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.pratta
        (articul, link, name, description, link_material, name_material, price, complexity, price_for_work, colors, main_pic, default_pic, systems, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (id, link, name, description, link_material, name_material, price, complexity, price_for_work, db_colors, main_pic, default_pic, db_system, today_time))
        cursor.close()
        connect.close()






def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    return response.text



def get_calalogue(html):
    catalogue = []
    soup = bs(html, 'lxml')

    # Верхняя строка каталога
    top_header = soup.find('nav', id='block-interiorsusage')\
    .find('ul', class_='menu menu--interiors-usage nav')\
    .find_all('li')
    for top_element in top_header:
        top_element = top_element.find('a').get('href')
        print(top_element)
        catalogue.append(top_element)

    # Нижняя строка каталога
    bot_header = soup.find('section', id='block-views-block-interior-effects-type-block-1')\
    .find('div', class_='view-content').find_all('div', class_='views-row')
    for bot_element in bot_header:
        bot_element = bot_element.find('h2').find('a').get('href')
        print(bot_element)
        catalogue.append(bot_element)
    return catalogue

list_products = []
def get_products(html):
    soup = bs(html, 'lxml')
    products = soup.find('div', class_='views-element-container form-group').find('div', class_='view-content')\
    .find_all('div', class_='views-row')
    for product in products:
        product = 'https://pratta.ru' + product.find('div').find('a').get('href')
        list_products.append(product)
        print(product)



def get_data(html):
    soup = bs(html, 'lxml')
    link = soup.find('link', rel='shortlink').get('href')

    id = soup.find('div', class_='interior-description').find('div', class_='field--item').text.strip()

    name = soup.find('div', class_='interior-description')\
    .find('div', class_='views-element-container form-group')\
    .find('div', class_='views-field views-field-title').find('h2').text.strip()

    try:
        description = soup.find('div', class_='interior-description')\
        .find('div', class_='field field--name-field-description field--type-string-long field--label-hidden field--item').text.strip()
    except:
        description = 'Нет описания'

    material = soup.find('div', class_='interior-description')\
    .find('div', class_='interior-material-group')\
    .find('div', class_='field field--name-field-link-to-material field--type-entity-reference field--label-inline')\
    .find('div', class_='field--item').find('a')
    link_material = material.get('href')
    name_material = material.text.strip()


    price = int(soup.find('div', class_='interior-description')\
    .find('div', class_='interior-material-group')\
    .find('div', class_='field field--name-field-price-for-interior-rub field--type-float field--label-inline')\
    .find('div', class_='field--item').get('content'))


    try:
        complexity = soup.find('div', class_='interior-description')\
        .find('div', class_='interior-work-group')\
        .find('div', class_='field field--name-field-complexity-work field--type-entity-reference field--label-inline')\
        .find('div', class_='field--item').text.strip()
    except:
        complexity = 'Проконсультируйтесь по данному покрытию или закажите его.'

    try:
        price_for_work = int(soup.find('div', class_='interior-description')\
        .find('div', class_='interior-work-group')\
        .find('div', class_='field field--name-field-price-rub field--type-float field--label-inline')\
        .find('div', class_='field--item').get('content'))
    except:
        price_for_work = None


    FINAL_picture_list = []
    pictures_first = soup.find('div', class_='field-group-tabs-wrapper').find('div', id='edit-group-colors')\
    .find('div', id='edit-group-colors--content').find_all('div', class_='field--item')
    for i in pictures_first:
        try:
            fpic = i.find('div', class_='field field--name-field-color-variant field--type-image field--label-hidden field--item').find('a').get('href') + ';; '
            FINAL_picture_list.append(fpic)
        except AttributeError:
            pass

    pictures_second = soup.find('div', class_='field-group-tabs-wrapper').find('div', id='edit-group-colors')\
    .find('div', class_='views-element-container form-group').find_all('div', class_='views-row')
    for j in pictures_second:
        try:
            lpic = (j.find('a').get('href')) + ';; '
            FINAL_picture_list.append(lpic)
        except AttributeError:
            pass




    main_pic = 'https://pratta.ru' + soup.find('div', class_='region region-content').find('article', class_='interiors full clearfix')\
    .find('div', class_='content').find('img').get('src')

    try:
        default_pic = soup.find('div', class_='field field--name-field-example field--type-image field--label-hidden field--item').find('a').get('href')
    except:
        default_pic = 'Null'

    tab_system = []
    SYSTEM = soup.find('div', id='edit-group-system').find('div', id='edit-group-system--content')\
    .find('div', class_='views-element-container form-group').find('div', class_='table-responsive')\
    .find('tbody').find_all('tr')
    for system in SYSTEM:
        system = system.find_all('td')
        for sys in system:
            try:
                sys = sys.find('a').get('href') + ' > ' + sys.text.strip().replace('        ', '').replace('        ', '').replace('        ', '').replace('        ','') + ';; '
                tab_system.append(sys)
            except:
                sys = sys.text.replace('        ', '').replace('        ', '').replace('        ', '').replace('        ','') + ';; '
                tab_system.append(sys)
        tab_system.append(' | ')



    data = {
        'id': id,                                       # id
        'link': link,                                   # Линк
        'name': name,                                   # Наименование
        'description': description,                     # Описание
        'link_material': link_material,                 # Линк на материал (где банка с краской)
        'name_material': name_material,                 # Имя этого материала
        'price': price,                                 # Цена руб/м2
        'complexity': complexity,                       # Сложность нанесения
        'price_for_work': price_for_work,               # Цена за работу руб/м2
        'colors': ''.join(FINAL_picture_list),          # Ссылки вкладки COLORS
        'main_pic': main_pic,                           # Основная картинка (Большая)
        'default_pic': default_pic,                     # Дефолтная картинка (Слева от описания, цен и тд)
        'system': ''.join(tab_system)                   # Вкладка SYSTEM в виде: n1>name;; n2;; n3;; n4;; | - конец табличной строки
    }

    today_time = str(datetime.date.today())
    db_colors = ''.join(FINAL_picture_list)
    db_system = ''.join(tab_system)


    print(data)
    connect_to_database(id, link, name, description, link_material, name_material, price, complexity, price_for_work,
                        db_colors, main_pic, default_pic, db_system, today_time)



    #csv_writer(data)



def main():
    headers = h

    url = 'https://pratta.ru/ideas-catalogue'
    # Full Catalogue
    catalogue = get_calalogue(get_html(url, headers))
    '''

    urls = [
        'https://pratta.ru/node/1316',
        'https://pratta.ru/node/1299',
        'https://pratta.ru/velvet-516',
        'https://pratta.ru/node/1307'
        ]
    for k in urls:
        get_data(get_html(k, headers))

    '''
    for i in catalogue:
        get_products(get_html(i, headers))
        sleep(0.7)

    print('Конец формирования списка товаров')

    for j in list_products:
        print('now ' + str(j))
        get_data(get_html(j, headers))
        sleep(0.8)


if __name__ == '__main__':
    main()