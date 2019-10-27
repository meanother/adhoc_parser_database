# -*- coding :utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re
import logging
import time
import csv
import sys
import datetime
import psycopg2

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
log = logging.getLogger()
reg = r'\d+'


def redactor_info(list):
    qw = []
    for row in list:
        for y in row:
            a = y + ' : ' + row[y] + '; '
            qw.append(a)
    return qw

filename = (time.asctime() + '_shop-hansgrohe.csv')
def csv_writer(data):
    with open(filename, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['art'],
            data['name'],
            data['price'],
            data['link'],
            data['description'],
            data['full_info'],
            data['img_list']
        ))

def connect_to_database(art, name, int_p, link, desc, db_info, db_pictures, today_time):
    connect = psycopg2.connect(dbname='parsing_db',
                               user='hansgrohe',
                               password='artpole',
                               host='192.168.1.132',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    cursor.execute('''
    INSERT INTO adhoc_parser.artpole
    (articul, name, size, price_1, price_2, info, pictures, download, parse_date) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (art, name, int_p, link, desc, db_info, db_pictures, today_time))
    cursor.close()
    connect.close()


'''
    data = {
        'art': art,
        'name': name,
        'price': int_p,
        'link': link,
        'description': desc,
        'full_info': ''.join(current_info),
        'img_list': ', '.join(img_list)
    }
    
    today_time = str(datetime.date.today())
    db_info = ''.join(current_info)
    db_pictures = ', '.join(img_list)
'''



def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    #print(response.status_code)
    #print(response.headers)
    if response.ok:
        return response.text


items_list = []
def get_data(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='column product-item__wrapper')
    for item in items:
        href = item.find('div',class_='product-item__image-section').find('a').get('href')
        items_list.append(href)
    print('after append, count final list = ' + str(len(items_list)) + ' urls')



def get_data_card(html):
    soup = bs(html, 'html.parser')
    link = soup.find('link', rel='canonical').get('href')
    name = soup.find('h1', class_='product-card__title').text.strip()
    art = soup.find('div', class_='product-card__sku product-card__sku_desktop').text.strip()
    #ar = re.findall(reg, art)
    #for a in ar:
    #    a = int(a)
    ''' Убрать регулярку, т.к. ид бывает интеджер '''
    try:
        price_off = soup.find('span', class_='price product1').text.replace(' ', '').replace('₽', '')
        int_p = int(price_off)
    except:
        int_p = None

    info = soup.find_all('div', class_='attribute-set')

    information = []
    for i in info:
        increment = i.find_all('div')
        for inc in increment:
            try:
                x1 = inc.find('dt').get('title')
                x2 = inc.find('dd').text
                dat = {x1 : x2}
                information.append(dat)
            except:
                pass

    current_info = redactor_info(information)

    img_list = []
    url_img = soup.find_all('li',class_='images-gallery__big-image-item overlay-container overlay-visible')
    for img in url_img:
        img_list.append(img.get('data-responsive').replace(' 800', '').replace('/800x', ''))

    try:
        description = soup.find('div', class_='description')
        desc = ((description.text).replace('•', ';').lstrip('; '))
    except:
        desc = 'Нет краткого описания'

    data = {
        'art': art,
        'name': name,
        'price': int_p,
        'link': link,
        'description': desc,
        'full_info': ''.join(current_info),
        'img_list': ', '.join(img_list)
    }

    today_time = str(datetime.date.today())
    db_info = ''.join(current_info)
    db_pictures = ', '.join(img_list)


    csv_writer(data)

    print(data)



def main():
    print('Start: ' + time.asctime())
    print('INFO: Parsing with 1 sec timeouts!')
    start_time = time.time()
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


    # Bathroom
    for x in range(1, 10):
        url = 'https://shop.hansgrohe.ru/vannaya-komnata/smesiteli?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/vannaya-komnata/dush?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/vannaya-komnata/aksessuary?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/vannaya-komnata/sistemy-skrytogo-montazha?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/vannaya-komnata/sifony?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/kukhnya/kombinacii-dlja-zony-mojki?p={}'.format(x)
        get_data(get_html(url, headers=headers))

        url = 'https://shop.hansgrohe.ru/kukhnya/smesiteli-dlja-kuhonnoj-mojki?p={}'.format(x)
        get_data(get_html(url, headers=headers))

    for i in items_list:
        get_data_card(get_html(i, headers=headers))
        time.sleep(0.2)

    end_time = time.time()
    print('parsing time, seconds: ', end_time - start_time)
    print('Finish: ' + time.asctime())


if __name__ == '__main__':
    main()
