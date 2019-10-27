import requests
from bs4 import BeautifulSoup as bs
from config import headers as h, LXM_list
import csv
from time import sleep
import pprint
import psycopg2
import datetime


def csv_writer(data):
    with open('Pergo_fix.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['link'],
            data['name'],
            data['articul'],
            data['garant'],
            data['pics'],
            data['feature1'],
            data['feature2'],
            data['download'],
            data['dop1'],
            data['dop2'],
            data['dop3'],
            data['dop4'],
            data['dop5'],
        ))

        '''
        'link': link,
        'name': name,
        'articul': articul,
        'garant': garant,
        'pics': ''.join(list_pics),
        'feature1': list_feature1,
        'feature2': list_feature2,
        'download': ''.join(list_downloads),
        'dop1': ''.join(list_cat1),
        'dop2': ''.join(list_cat2),
        'dop3': ''.join(list_cat3),
        'dop4': ''.join(list_cat4),
        'dop5': ''.join(list_cat5),
        '''


def connect_to_database(articul, name, link, garant, db_pics, db_feature1, db_feature2, db_download, db_dop1, db_dop2, db_dop3, db_dop4, db_dop5, today_time):
    connect = psycopg2.connect(dbname='parsing_db',
                               user='pergo',
                               password='pergo',
                               host='localhost',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    cursor.execute('''
    INSERT INTO adhoc_parser.pergo
    (articul, name, link, garant, pictures, feature_1, feature_2, download, extra_accessories_1,extra_accessories_2,extra_accessories_3 ,extra_accessories_4 ,extra_accessories_5, parse_date) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (articul, name, link, garant, db_pics, db_feature1, db_feature2, db_download, db_dop1, db_dop2, db_dop3, db_dop4, db_dop5, today_time))
    cursor.close()
    connect.close()


def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    if response.ok:
        #print(response.text)
        return response.text


list_cards = []
BONUS = []


def get_another_cards(html):
    soup = bs(html, 'lxml')
    all_cards = soup.find('div', class_='row u-row-flex u-gutter-small-until-tablet').find_all('div', class_='col-md-4 col-sm-4 col-xs-6 col-xxs-12')
    for card in all_cards:
        card = 'https://www.pergo.ru' + card.find('a').get('href')
        list_cards.append(card)
    print(len(all_cards))


def getin_card(html):
    soup = bs(html, 'lxml')

    try:
        link = soup.find('link', rel='canonical').get('href')
    except:
        link = 'NULL'
    try:
        name = soup.find('div', attrs= {'data-webid': 'productinfo-carousel-title'}).find('h1').text.strip()
    except:
        name = 'NULL'

    try:
        articul = soup.find('div', attrs= {'data-webid': 'productinfo-carousel-title'}).find('span').text.strip()
    except:
        articul = 'NULL'

    try:
        garant = soup.find('div', class_='c-product-detail__usp-list row u-mt-1 u-mb-1 hidden-xs').text.strip().replace('\n', '; ').replace('; ; ; ; ', '').replace('\t', '; ')
    except:
        garant = 'NULL'

    list_pics = []
    try:
        pics = soup.find('div', attrs={'data-component-class': 'Dlw.ScBase.Flooring.FloorInfoCarousel'})\
            .find('div', class_='row')\
            .find('div', class_='c-product-detail__slider')\
            .find('section', class_='c-slider c-slider-project c-slider--detail')\
            .find('div', attrs={'data-selector': 'product-detail-slider'}).find_all('a')
        for pic in pics:
            pic = pic.get('href')
            list_pics.append(pic + ', ')
    except:
        try:
            ex_pics = soup.find('div', attrs={'data-selector': 'product-detail-slider'}).find_all('a')
            for ex_pic in ex_pics:
                ex_pic = ex_pic.get('href')
                list_pics.append(ex_pic + ', ')
        except:
            list_pics = ['NULL']

    list_feature1 = []
    try:
        stats = soup.find('div', attrs={'data-webid': 'productdetails-specifications'})\
            .find('div', class_='collapse')\
            .find_all('tbody', attrs={'data-webid': 'specification-block'})

        feature1 = stats[0].find_all('tr')
        for f1 in feature1:
            f1 = f1.text.strip().replace('\n', ': ') + '; '
            list_feature1.append(f1)
        #print(list_feature1)
    except:
        list_feature1 = ['NULL']


    try:
        list_feature2 = []
        stats = soup.find('div', attrs={'data-webid': 'productdetails-specifications'}) \
            .find('div', class_='collapse') \
            .find_all('tbody', attrs={'data-webid': 'specification-block'})

        feature2 = stats[1].find_all('tr')
        for f2 in feature2:
            f2 = f2.text.strip().replace('\n', ': ') + '; '
            f2 = f2.replace('\r: \t.c-svg--custom {}', '').replace(': : ; ', '')
            list_feature2.append(f2)
        #print(list_feature2)
    except:
        list_feature2 = ['NULL']

    list_downloads = []
    try:
        downloads = soup.find('div', id='collapseDocuments').find_all('li')
        for download in downloads:
            download = 'https://www.pergo.ru' + download.find('a').get('href') + ', '
            #print(download)
            list_downloads.append(download)
    except:
        list_downloads = ['NULL']

    # Дополнительные товары под парсинг


    '''
    for R in references:
        xme = references.find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        for xm in xme:
            index = 0
            xm = 'https://www.pergo.ru' + xm.find('a').get('href')
            print(xm)
            BONUS.append(xm)
        print('----------\n')
    '''





    try:
        references = soup.find('div', class_='c-tabs c-tabs--collapse@desktop').find('div', class_='c-tabs__content').find_all('div', attrs={'data-webid': '#accessory-group'})

        cat1 = references[0].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        list_cat1 = []
        for c1 in cat1:
            id1 = c1.find('div', class_='c-card__body u-bg-white').find('div', attrs={'data-webid': 'accessory-subtitle'}).find('span', class_='c-card__sub-ttl--code').text
            c1 = 'https://www.pergo.ru' + c1.find('a').get('href')
            list_cat1.append(id1 + ', ')
            BONUS.append(c1)
    except:
        list_cat1 = ['NULL']


    try:
        references = soup.find('div', class_='c-tabs c-tabs--collapse@desktop').find('div', class_='c-tabs__content').find_all('div', attrs={'data-webid': '#accessory-group'})

        cat2 = references[1].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        list_cat2 = []
        for c2 in cat2:
            id2 = c2.find('div', class_='c-card__body u-bg-white').find('div', attrs={'data-webid': 'accessory-subtitle'}).find('span', class_='c-card__sub-ttl--code').text
            c2 = 'https://www.pergo.ru' + c2.find('a').get('href')
            list_cat2.append(id2 + ', ')
            BONUS.append(c2)
    except:
        list_cat2 = ['NULL']


    try:
        references = soup.find('div', class_='c-tabs c-tabs--collapse@desktop').find('div', class_='c-tabs__content').find_all('div', attrs={'data-webid': '#accessory-group'})

        cat3 = references[2].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        list_cat3 = []
        for c3 in cat3:
            id3 = c3.find('div', class_='c-card__body u-bg-white').find('div', attrs={'data-webid': 'accessory-subtitle'}).find('span', class_='c-card__sub-ttl--code').text
            c3 = 'https://www.pergo.ru' + c3.find('a').get('href')
            list_cat3.append(id3 + ', ')
            BONUS.append(c3)
    except:
        list_cat3 = ['NULL']


    try:
        references = soup.find('div', class_='c-tabs c-tabs--collapse@desktop').find('div', class_='c-tabs__content').find_all('div', attrs={'data-webid': '#accessory-group'})

        cat4 = references[3].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        list_cat4 = []
        for c4 in cat4:
            id4 = c4.find('div', class_='c-card__body u-bg-white').find('div', attrs={'data-webid': 'accessory-subtitle'}).find('span', class_='c-card__sub-ttl--code').text
            c4 = 'https://www.pergo.ru' + c4.find('a').get('href')
            list_cat4.append(id4 + ', ')
            BONUS.append(c4)
    except:
        list_cat4 = ['NULL']


    try:
        references = soup.find('div', class_='c-tabs c-tabs--collapse@desktop').find('div', class_='c-tabs__content').find_all('div', attrs={'data-webid': '#accessory-group'})

        cat5 = references[4].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div', attrs={'data-webid': '#accessory'})
        list_cat5 = []
        for c5 in cat5:
            id5 = c5.find('div', class_='c-card__body u-bg-white').find('div', attrs={'data-webid': 'accessory-subtitle'}).find('span', class_='c-card__sub-ttl--code').text
            c5 = 'https://www.pergo.ru' + c5.find('a').get('href')
            list_cat5.append(id5 + ', ')
            BONUS.append(c5)
    except:
        list_cat5 = ['NULL']



    #name_ref0 = references[0].find('h3').text.strip()
    '''
    links_ref0 = references[0].find('div', class_='o-box o-box--flush collapse').find('div', class_='row u-row-flex').find_all('div')
    for link_ref0 in links_ref0:
        link_ref0 = 'https://www.pergo.ru' + link_ref0.find('a').get('href')
        BONUS.append(link_ref0)
        print(link_ref0)
    '''



    '''
    list_feature = []
    for feature in feature1:
        try:
            feature_key = feature.find('td').text.strip()
        except:
            feature_key = 'Заголовок'
        try:
            feature_value = feature.find('td', attrs={'data-webid': 'specificationattribute-value'}).text.strip()
        except:
            feature_value = 'Заголовок'

        xfeature = {feature_key: feature_value}
        list_feature.append(xfeature)
        print(xfeature)
    '''


    data = {
        'link': link,
        'name': name,
        'articul': articul,
        'garant': garant,
        'pics': ''.join(list_pics),
        'feature1': ''.join(list_feature1),
        'feature2': ''.join(list_feature2),
        'download': ''.join(list_downloads),
        'dop1': ''.join(list_cat1),
        'dop2': ''.join(list_cat2),
        'dop3': ''.join(list_cat3),
        'dop4': ''.join(list_cat4),
        'dop5': ''.join(list_cat5),
    }

    db_pics = ''.join(list_pics)
    db_feature1 = ''.join(list_feature1)
    db_feature2 = ''.join(list_feature2)
    db_download = ''.join(list_downloads)
    db_dop1 = ''.join(list_cat1)
    db_dop2 = ''.join(list_cat2)
    db_dop3 = ''.join(list_cat3)
    db_dop4 = ''.join(list_cat4)
    db_dop5 = ''.join(list_cat5)
    today_time = str(datetime.date.today())




    print(data)
    connect_to_database(articul, name, link, garant, db_pics, db_feature1, db_feature2, db_download, db_dop1, db_dop2,
                        db_dop3, db_dop4, db_dop5, today_time)
    #csv_writer(data)
    #pprint.pprint(data)




def main():

    urls = [
        'https://www.pergo.ru/ru-RU/%D0%BD%D0%B0%D0%B9%D0%B4%D0%B8%D1%82%D0%B5-%D1%81%D0%B2%D0%BE%D0%B9-%D0%BF%D0%BE%D0%BB?filter=FloorTypeCode.eq.lmp&page=3&page_size=24&view_size=72',
        'https://www.pergo.ru/ru-RU/%D0%BD%D0%B0%D0%B9%D0%B4%D0%B8%D1%82%D0%B5-%D1%81%D0%B2%D0%BE%D0%B9-%D0%BF%D0%BE%D0%BB?filter=FloorTypeCode.eq.lvt&page=3&page_size=24&view_size=72'
    ]

    headers = h

    for url in urls:
        get_another_cards(get_html(url, headers))
        sleep(1)
    print('Конец забора ссылок с 3 основных страниц')

    for x in list_cards:
        print(x)
        getin_card(get_html(x, headers))
        sleep(0.5)
    print('Конец забора ссылок на карточки с основного списка\n')

    print('Кол-во элементов в листе C дублями: ' + str(len(BONUS)))
    clear_BONUS = set(BONUS)
    print('Кол-во элементов в листе без дублей: ' + str(len(clear_BONUS)))

    for j in clear_BONUS:
        print(j)
        getin_card(get_html(j, headers))
        sleep(0.5)
    print('Конец парсинга дополнительных товаров')

    #bx = 'https://www.pergo.ru/ru-RU/%D0%BB%D0%B0%D0%BC%D0%B8%D0%BD%D0%B0%D1%82/modern-plank-sensation/l1231-03369_%D0%BD%D0%BE%D0%B2%D1%8B%D0%B8-%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B8%D1%81%D0%BA%D0%B8%D0%B8-%D0%B4%D1%83%D0%B1-%D0%BF%D0%BB%D0%B0%D0%BD%D0%BA%D0%B0'
    #getin_card(get_html(bx, headers))



if __name__ == '__main__':
    main()







