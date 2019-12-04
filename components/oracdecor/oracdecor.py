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
from selenium import webdriver
from kafka import KafkaProducer, KafkaConsumer
import datetime



def csv_writer(data):
    with open('/home/arty/python/adhoc_parser/components/oracdecor/oracdecor.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['name'],
            data['category'],
            data['specifications'],
            data['available_text'],
            data['overview'],
            data['scheme_picture'],
            data['banner'],
            data['max_tag'],
            data['price_metr'],
            data['price_one'],
            data['big_pic'],
            data['text'],
            data['pdfs'],
            data['link']
        ))


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))



def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    #print(response.text)
    return response.text

# Возвращает 6 категорий товаров
def get_store_menu(html):
    list_menu = []
    soup = bs(html, 'lxml')
    store_menu = soup.find('div', id='store.menu').find('nav', class_='navigation').find('ul').find_all('li')
    for store in store_menu:
        try:
            store = store.find('a').get('href')
            list_menu.append(store)
        except AttributeError:
            pass
    print(list_menu)
    return list_menu


# Return list cards from page
final_list_cards = []
def get_cards(html):
    soup = bs(html, 'lxml')
    cards = soup.find('div', class_='products wrapper grid products-grid').find('ol').find_all('li')
    for card in cards:
        card = card.find('a').get('href')
        final_list_cards.append(card)
        print(card)


list_flex = []
def get_data(card, html):
    if 'karnizy' in card:
        category = 'Карнизы'
    elif 'plintusy' in card:
        category = 'Плинтус'
    elif 'moldingi' in card:
        category = 'Молдинг'
    elif 'skrytoe-osveschenie' in card:
        category = 'Скрытое освещение'
    elif 'dekorativnye-elementy' in card:
        category = 'Декоративные элементы'
    elif 'klei-i-instrumenty' in card:
        category = 'Клеи и инструменты'

    #print(category)

    soup = bs(html, 'lxml')
    name = soup.find('div', class_='category-colors').find('div', class_='page-title-wrapper product').text.strip()
    #print(name)
    try:
        specifications = soup.find('div', class_='specifications').text.strip().replace('\n', '').replace('        ', ' ')
    except:
        specifications = ''
    #print(specifications)
    try:
        available = soup.find('div', class_='specifications').find('a').get('href')
        list_flex.append(available)
    except:
        available = ''
    try:
        available_text = soup.find('div', class_='specifications').find('a').text.strip()
        #print(available_text)
    except:
        available_text = ''

    try:
        overview = soup.find('div', class_='product attribute desktop overview').find('div').text.strip()
        #print(overview)
    except:
        overview = ''
    try:
        scheme_picture = soup.find('div', class_='product-info-cross-section-image desktop').find('img').get('src')
        #print(scheme_picture)
    except:
        scheme_picture = ''
    try:
        banner = soup.find('div', class_='usp-banner').find('div', class_='row').find('div').text.strip().replace('\n', ' ')
        #print(banner)
    except:
        banner = ''

    try:
        max_tag = soup.find('meta', itemprop='image').get('content')
        #print(max_tag)
    except:
        max_tag = ''
    try:
        price_metr = soup.find('div', class_='product-info-price').find('span', class_='price-wrapper').get('data-price-amount')
    except:
        price_metr = ''

    try:
        price_one = soup.find('div', class_='product-info-price').find('span', class_='price-detail final-price')\
        .find('span', class_='price-wrapper').get('data-price-amount')
    except:
        price_one = ''
    #print(price_metr)
    #print(price_one)
    pdf_list = []
    try:
        pdf = soup.find('div', class_='tools-technical-container').find('div', class_='col-md-6 technical-specifications')\
        .find('div', class_='product-assets').find_all('div', class_='asset-group multiple')
        for row in pdf:
            rows = row.find('div', class_='group-content').find_all('div', class_='asset-files-wrapper')
            for file in rows:
                file_name = file.find('a').text.strip()
                https_link = file.find('a').get('href')
                if 'pdf' in file_name:
                    pdf_link = file_name + ' : ' + https_link
                    pdf_list.append(pdf_link)
        #print(pdf_list)
        db_pdf_list = ' : '.join(pdf_list)
    except:
        db_pdf_list = ' : '.join(pdf_list)
    #print(db_pdf_list)



    try:
        big_pic = soup.find('div', class_='markers').find('img', class_='pinable').get('src')
        #(big_pic)
    except AttributeError:
        try:
            big_pic = soup.find('div', class_='inspiration-product-detail').find('div', class_='container').find('img', class_='pinable').get('src')
            #print(big_pic)
        except:
            big_pic = ''

    try:
        text = soup.find('div', class_='value block product-list-block product-cols-3').text.strip().replace('\n', ' ;; ')
        # print(text)
    except:
        text = ''
    try:
        link = soup.find('link', rel='canonical').get('href')
        #print(link)
    except:
        link = ''

    today_time = str(datetime.date.today())

    data ={
        'name': name,
        'category': category,
        'specifications': specifications,
        'available_text': available_text,
        'overview': overview,
        'scheme_picture': scheme_picture,
        'banner': banner,
        'max_tag': max_tag,
        'price_metr': price_metr,
        'price_one': price_one,
        'big_pic': big_pic,
        'text': text,
        'pdfs': db_pdf_list,
        'link': link,
        'parse_date': today_time
    }
    print(data)

    producer.send('oracdecor', key=b'row_oracdecor', value=data)
    #connect_to_database(name, category, specifications, available_text, overview, scheme_picture, banner, max_tag, price_metr, price_one, big_pic, text, db_pdf_list, link, today_time)


def main():
    headers = h

    url = 'https://oracdecor.ru/'
    tabs = get_store_menu(get_html(url, headers))
    print(tabs)

    for tab in tabs:
        print('this is tab: ' + tab)
        for index in range(1, 20):
            get_cards(get_html(tab+f'?p={index}', headers))
            sleep(0.2)

    print('length of first list: ' + str(len(final_list_cards)))
    print('length of set list: ' + str(len(set(final_list_cards))))
    for card in set(final_list_cards):
        print(card)
        get_data(card, (get_html(card, headers)))
        sleep(0.6)

    #get_cards(get_html(url, headers))
    '''
    urls = [
        'https://oracdecor.ru/plintusy/sx138f_skirting',
        'https://oracdecor.ru/karnizy/c391_cornice_moulding',
        'https://oracdecor.ru/moldingi/p4020_panel_moulding',
        'https://oracdecor.ru/skrytoe-osveschenie/c380_uplighter'
    ]
    for url in urls:
        get_data(url, (get_html(url, headers)))
        sleep(0.1)
        print('-------')
    '''


if __name__ == '__main__':
    main()