import requests
from bs4 import BeautifulSoup as bs
import csv
from config import headers as h
import pprint
from time import sleep




def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    if response.ok:
        #print(response.text)
        return response.text


def get_catalog(html):
    list_catalog = []
    soup = bs(html, 'lxml')
    cards = soup.find('div', class_='panel-body').find_all('ul', class_='nav_n')
    for card in cards:
        try:
            card = card.find('ul', id='nav').find_all('li')
            for c in card:
                c = 'https://wasserkraft.ru/' + c.find('a').get('href')
                list_catalog.append(c)
                #print(c)
        except AttributeError:
            pass
    return list_catalog



def get_products(html):
    list_products = []
    soup = bs(html, 'lxml')
    pd = soup.find_all('div', class_='panel panel-default no-border-top')
    print(len(pd[2]))
    #print(pd[2])
    for p in pd[2]:
        print(p.find_all('div'))
        '''
        p = p.find_all('div', class_='serie_items itemsheight col-xs-6')
        for x in p:
            x = x.find('div', class_='media').find('a').get('href')
            print(x)
        '''

#https://wasserkraft.ru/vyivod-iz-assortimenta


def main():
    headers = h
    '''
    url = 'https://wasserkraft.ru/products/'
    get_catalog(get_html(url, headers))
    temp_1 = get_catalog(get_html(url, headers))
    '''


    #for j in temp_1:
    #    print(str(j) + '\n')

    k = 'https://wasserkraft.ru/rhin-4403'
    get_products(get_html(k, headers))

if __name__ == '__main__':
    main()
