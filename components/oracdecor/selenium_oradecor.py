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


b = webdriver.Chrome()
b.implicitly_wait(15)


def get_html(url):
    b.get(url)
    sleep(5)
    return b.page_source


# Возвращает 6 категорий товаров
def get_store_menu(html):
    store_menu = []
    soup = bs(html, 'lxml')
    store_menu = soup.find('div', id='store.menu').find('nav', class_='navigation').find('ul').find_all('li')
    for store in store_menu:
        store = store.find('a').get('href')
        store_menu.append(store)
    return store_menu


# Return list cards from page
def get_cards(html):
    list_cards = []
    soup = bs(html, 'lxml')
    cards = soup.find('div', class_='products wrapper grid products-grid').find('ol').find_all('li')
    for card in cards:
        card = card.find('a').get('href')
        print(card)
        list_cards.append(card)
    return list_cards

list_flex = []
def get_data(html):
    soup = bs(html, 'lxml')
    name = soup.find('div', class_='category-colors').find('div', class_='page-title-wrapper product').text.strip()
    print(name)
    specifications = soup.find('div', class_='specifications').text.strip().replace('\n', '').replace('        ', ' ')
    print(specifications)
    available = soup.find('div', class_='specifications').find('a').get('href')
    list_flex.append(available)
    available_text = soup.find('div', class_='specifications').find('a').text.strip()
    print(available_text)
    overview = soup.find('div', class_='product attribute desktop overview').find('div').text.strip()
    print(overview)
    scheme_picture = soup.find('div', class_='product-info-cross-section-image desktop').find('img').get('src')
    print(scheme_picture)
    banner = soup.find('div', class_='usp-banner').find('div', class_='row').find('div').text.strip().replace('\n', ' ')
    print(banner)

    main_pic = soup.find('div', class_='gallery-placeholder')\
    .find('div', attrs={'data-gallery-role':'gallery'}).find('div', class_='fotorama__stage__shaft')\
    .find('div').get('href')
    print(main_pic)



def main():
    headers = h
    '''
    url = 'https://oracdecor.ru/plintusy?p=2'
    get_cards(get_html(url, headers))
    '''
    urls = [
        'https://oracdecor.ru/plintusy/sx138f_skirting',
        'https://oracdecor.ru/karnizy/c391_cornice_moulding',
        'https://oracdecor.ru/moldingi/p4020_panel_moulding',
        'https://oracdecor.ru/skrytoe-osveschenie/c380_uplighter'
    ]
    for url in urls:
        get_data(get_html(url))
        print('---------')


if __name__ == '__main__':
    main()