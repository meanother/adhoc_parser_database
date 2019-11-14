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

list_accessory = []


def csv_writer(data):
    with open('/home/arty/python/adhoc_parser/components/stilye/stilye.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['id'],
            data['name_first'],
            data['name_second'],
            data['picture'],
            data['main_picture'],
            data['price'],
            data['coating'],
            data['category'],
            data['description'],
            data['equipment'],
            data['accessory'],
        ))


def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    #print(response.text)
    return response.text


list_data = []
def get_data(html):
    soup = bs(html, 'lxml')
    orders = soup.find('section', class_='site-section productList thin-paragraphs')\
    .find('div', class_='container').find('div', class_='productList-products').find_all('div')
    for order in orders:
        order = 'http://www.stilye.ru' + order.find('a').get('href')
        print(order)
        list_data.append(order)


def get_order_info(html):
    soup = bs(html, 'lxml')
    name = soup.find('h1').text.strip()
    category = soup.find('div', class_='breadcrumbs').find('a').text.strip()
    try:
        main_pic = 'http://www.stilye.ru' + soup.find('div', class_='imageWrapper-media intImage').find('img').get('src')
    except AttributeError:
        main_pic = 'http://www.stilye.ru' + soup.find('div', class_='productDetail-info_images').find('img').get('src')

    list_description = []
    try:
        description = soup.find('section', class_='productDetail-descriptionSection').find('ul', class_='productDetail-description-list').find_all('li')
        for desc in description:
            try:
                desc = 'http://www.stilye.ru' + desc.find('a').get('href') + ' ;; '
                list_description.append(desc)
            except:
                desc = desc.text + ' ;; '
                list_description.append(desc)
        ready_description = ''.join(list_description)
    except AttributeError:
        ready_description = None

    list_equipment = []
    try:
        equipment = soup.find('section', class_='productDetail-includeSection').find('ul').find_all('li')
        for equip in equipment:
            list_equipment.append(equip.text + ' ;; ')
        ready_equipment = ''.join(list_equipment)
    except AttributeError:
        ready_equipment = None


    components = soup.find('section', class_='productDetail-price site-section').find('div', class_='productDetail-price_tableWrapper').find_all('tr')[1:]
    for component in components:
        component = component.find_all('td')
        try:
            jpeg_component = 'http://www.stilye.ru' + component[0].find('a').get('href')
        except AttributeError:
            jpeg_component = None
        id_component = component[1].text.strip()
        name_component = component[2].text.strip()
        coating_component = None
        try:
            price_component = int(component[3].text.strip())
        except ValueError:
            try:
                coating_component = (component[3].text.strip())
                price_component = int(component[4].text.strip())
            except IndexError:
                try:
                    price_component = int(component[3].text.strip())
                except ValueError:
                    xregex = r' \d+'
                    price_component = int(''.join(re.findall(xregex, component[3].text.strip())).replace(' ', ''))

                # Сделать регулярку для второй цены (скидка)
        #print(jpeg_component)
        #print(id_component)
        #print(name_component)
        #print(price_component)


        column_accessory = []
        try:
            accessory = soup.find('section', class_='productDetail-additional productDetail-additional--big site-section')\
            .find_all('section')
            for section in accessory:
                for item in section:
                    item = 'http://www.stilye.ru' + item.find('a').get('href')
                    itemx = item + ' ;; '
                    column_accessory.append(itemx)
                    #print(itemx)
                    #print(itemx)
                    list_accessory.append(item)
                    #print(item)
            db_column_accessory = ''.join(column_accessory)
        except AttributeError:
            try:
                accessory = soup.find('section', class_='productDetail-additional productDetail-additional_accessories site-section')\
                .find('section', class_='product-canUseWater')
                for item in accessory:
                    item = 'http://www.stilye.ru' + item.find('a').get('href')
                    itemx = item + ' ;; '
                    column_accessory.append(itemx)
                    #print(itemx)
                    # print(itemx)
                    list_accessory.append(item)
                    #print(item)
                db_column_accessory = ''.join(column_accessory)
            except:
                db_column_accessory = None


        #print(name)
        #print(category)
        #print(main_pic)
        #print(ready_description)
        #print(ready_equipment)


        data = {
            'id': id_component,
            'name_first': name,
            'name_second': name_component,
            'picture': jpeg_component,
            'main_picture': main_pic,
            'price': price_component,
            'coating': coating_component,
            'category': category,
            'description': ready_description,
            'equipment': ready_equipment,
            'accessory': db_column_accessory
        }
        print(data)
        csv_writer(data)


def main():
    headers = h
    urls = ['http://www.stilye.ru/productions/accessories/',
            'http://www.stilye.ru/productions/water/',
            'http://www.stilye.ru/productions/electric/',
            'http://www.stilye.ru/productions/additional/']

    for url in urls:
        print(url)
        get_data(get_html(url, headers))
        print('-----')

    for data_url in set(list_data):
        print(data_url)
        get_order_info(get_html(data_url, h))
        sleep(0.7)

    for accessory in set(list_accessory):
        print(accessory)
        get_order_info((get_html(accessory, h)))
        sleep(0.7)

    # Test items
    '''
    urls = [
        'http://www.stilye.ru/productions/electric/infodetail.php?IB=8&IP=637373',
        'http://www.stilye.ru/productions/additional/infodetail.php?IB=21&IP=637536',
        'http://www.stilye.ru/productions/water/infodetail.php?IB=7&IP=637309',
        'http://www.stilye.ru/productions/accessories/infodetail.php?IB=74&IP=637864',
        'http://www.stilye.ru/productions/water/infodetail.php?IB=7&IP=637329'
    ]
    for url in urls:
        print(url)
        get_order_info(get_html(url, headers))
        print('---------')
    '''


if __name__ == '__main__':
    main()