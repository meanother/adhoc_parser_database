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


def get_catalog(html):
    x = []
    soup = bs(html, 'lxml')
    catalogs = soup.find('div', class_='products').find_all('form')
    for catalog in catalogs:
        catalog = 'https://letique.ru/' + catalog.find('a').get('href')
        x.append(catalog)
        print(catalog)
    return x


def get_data(html):
    soup = bs(html, 'lxml')
    f = open('lisa.txt', 'a')
    name = soup.find('h1', class_='page__title').text.strip()
    f.write(name)
    print(name)
    f.write('\n')


    # first block
    description_1 = soup.find('div', class_='col-40 item-page__right').find_all('p')[0].text.strip()
    f.write(description_1)
    print(description_1)
    f.write('\n')


    # second block
    try:
        description_2 = soup.find('div', class_='col-40 item-page__right').find_all('p')[1].text.strip()
        print(description_2)
        f.write(description_2)
        f.write('\n')

    except:
        pass

    # massa
    try:
        massa = soup.find('div', class_='col-40 item-page__right').find('form', class_='product__data ms2_form')\
        .find('div', class_='product__desc product__desc--item').text.strip()
        print(massa)
        f.write(massa)
        f.write('\n')

    except:
        massa = 'Масса не указана'
        print(massa)
        f.write(massa)
        f.write('\n')

    # price
    price = soup.find('div', class_='col-40 item-page__right').find('form', class_='product__data ms2_form')\
    .find('div', class_='product__price product__price--item').text.strip()
    print(price)
    f.write(price)
    f.write('\n')



    # engridients
    try:
        description_3 = soup.find('div', class_='title title--ingredients').text.strip()
        print(description_3)
        f.write(description_3)
        f.write('\n')

    except:
        description_3 = 'Нет ингридиентов'
        print(description_3)
        f.write(description_3)
        f.write('\n')

    # ingredients
    description_4 = soup.find('div', class_='ingredients ingredients--item').find_all('div', class_='ingredient')
    for desc4 in description_4:
        desc4 = desc4.find('div', class_='ingredient__desc').text.strip()
        print(desc4)
        f.write(desc4)
        f.write('\n')

    # effects
    effect = soup.find('div', class_='title title--effects').text.strip()
    print(effect)
    f.write(effect)
    f.write('\n')


    # effect desc
    effect_desc = soup.find('div', class_='page__content page__content--item').find('div', class_='clearfix').find_all('div')
    for eff in effect_desc:
        eff = eff.text.strip()
        print(eff)
        f.write(eff)
        f.write('\n')

    # use
    use = soup.find('h3', class_='title title--ingredients').text.strip()
    print(use)
    f.write(use)
    f.write('\n')


    # use info
    section_use = soup.find('section', class_='quality').find('div', class_='clearfix').find_all('div')
    for suse in section_use:
        suse = suse.text.strip()
        print(suse)
        f.write(suse)
        f.write('\n')

    f.write('\n------------------\n')
    f.close()


def main():
    headers = h
    url = 'https://letique.ru/catalog/'
    catalogs = get_catalog(get_html(url, headers))
    for x in catalogs:
        print(x)
        get_data(get_html(x, headers))
        # break


if __name__ == '__main__':
    main()