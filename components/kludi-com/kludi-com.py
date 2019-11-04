#!/usr/bin/python3
# -*- coding :utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import re
import logging
import time
import csv
import datetime
import psycopg2
import json


#filename = str((time.asctime() + '_kludi.csv'))
filename = 'Fixed_kludi.csv'
def csv_writer(data):
    with open(filename, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['articul'],
            data['link'],
            data['jpeg'],
            data['size'],
            data['data_sheet']
        ))

def connect_to_database(articul, link, jpeg, size, data_sheet ,today_time):
    #with open('config.json', 'r') as file1:
    with open('/home/ubpc/adhoc_parser_database/components/kludi-com/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
                                   user=data['user'],
                                   password=data['password'],
                                   host=data['host'],
                                   port=data['port'])
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.kludi_com
        (articul, link, jpegs, size, data_sheet, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s)''', (articul, link, jpeg, size, data_sheet, today_time))
        cursor.close()
        connect.close()

'''
        'articul': articul,
        'link': link,
        'jpeg': jpeg,
        'size': size,
        'data_sheet': data_sheet
'''




def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.ok:
        #print(response.text)
        return response.text

urls = []
def get_urls(html):
    soup = bs(html, 'lxml')
    cards = soup.find_all('a', class_='category-filter-item-img')
    for card in cards:
        card = card.get('href')
        urls.append(card)
    print(len(urls))



def get_info(html):
    soup = bs(html, 'lxml')
    link1 = soup.find('div', class_='breadcrumbs').find_all('li')
    link = link1[-1].find('a').get('href')
    articul = soup.find('div', class_='dot-list-container').find('ul').text.strip()
    jpeg = soup.find('div', class_='button-container').find('a').get('href')
    try:
        size = soup.find('li', class_='product-dimensioned-drawing').find('a').get('href')
    except:
        size = 'not link to size'
    try:
        data_sheet = soup.find('li', class_='product-data-sheet').find('a').get('href')
    except:
        data_sheet = 'no link to data'
    data = {
        'articul': articul,
        'link': link,
        'jpeg': jpeg,
        'size': size,
        'data_sheet': data_sheet
    }
    today_time = str(datetime.date.today())

    print(data)
    connect_to_database(articul, link, jpeg, size, data_sheet, today_time)
    #csv_writer(data)
    #print(jpeg)


#bath - page 9 -        https://www.kludi.com/shop/ru/bath?p=1
#kitchen - page 2       https://www.kludi.com/shop/ru/kitchen?p=2
#shower - page 4        https://www.kludi.com/shop/ru/shower?p=4
def main():
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    # get urls to cards
    for x in range(16):
        url = 'https://www.kludi.com/shop/ru/bath?p={}'.format(x)
        get_urls(get_html(url, headers=headers))
    for x in range(5):
        url = 'https://www.kludi.com/shop/ru/kitchen?p={}'.format(x)
        get_urls(get_html(url, headers=headers))
    for x in range(8):
        url = 'https://www.kludi.com/shop/ru/shower?p={}'.format(x)
        get_urls(get_html(url, headers=headers))

    #https://www.kludi.com/shop/ru/catalogsearch/result/index/?p=13&q=%D1%81%D0%BC%D0%B5%D1%81%D0%B8%D1%82%D0%B5%D0%BB%D1%8C
    for x in range(15):
        url = 'https://www.kludi.com/shop/ru/catalogsearch/result/index/?p={}&q=%D1%81%D0%BC%D0%B5%D1%81%D0%B8%D1%82%D0%B5%D0%BB%D1%8C'.format(x)
        get_urls(get_html(url, headers=headers))

    # get full info
    for url in urls:
        get_info(get_html(url, headers=headers))
        time.sleep(0.2)
'''
case:
1) articul
2) url jpeg (Большую)
3) url for 2 files (Только размер и техкарта)
'''




if __name__ == '__main__':
    main()



