import requests
from bs4 import BeautifulSoup as bs
from config import headers as h, LXM_list
import csv
from time import sleep
import datetime
import psycopg2


def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    if response.ok:
        #print(response.text)
        return response.text


second_urls = []
def get_list(html):
    soup = bs(html, 'lxml')
    urls = soup.find('div', class_='left-menu').find_all('ul')
    for url in urls:
        url = 'https://www.artpole.ru' + url.find('a').get('href')
        print(url)
        second_urls.append(url)


def redactor_info(list):
    qw = []
    for row in list:
        for y in row:
            a = y + ' : ' + row[y] + '; '
            qw.append(a)
    return qw


def csv_writer(data):
    with open('Artpole_csv.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['name'],
            data['id'],
            data['size'],
            data['price_1'],
            data['price_2'],
            data['stats'],
            data['url_pic'],
            data['final_info']
        ))


def connect_to_database(art, na, ss, pr1, pr2, db_stats, db_info, pic, today_time):
    connect = psycopg2.connect(dbname='parsing_db',
                               user='artpole',
                               password='artpole',
                               host='192.168.1.132',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    cursor.execute('''
    INSERT INTO adhoc_parser.artpole
    (articul, name, size, price_1, price_2, info, pictures, download, parse_date) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (art, na, ss, pr1, pr2, db_stats, db_info, pic, today_time))
    cursor.close()
    connect.close()




def get_list_cards(html):
    with open('artpole_url_list.txt', 'a') as file:
        soup = bs(html, 'lxml')
        flexes = soup.find('div', class_='content').find('div', class_='collection new-style-collention flex-tempalte').find('div', class_='flex-tempalte-tbody').find_all('div', class_='template-line two-show-element-sect')
        for flex in flexes:
            flex = 'https://www.artpole.ru' + flex.find('a').get('href')
            file.write(flex + '\n')


def get_data(html):
    soup = bs(html, 'lxml')
    name = soup.find_all('div', class_='sostav-item-name')
    for na in name:
        na = na.text.strip()
        #print(na)
    try:
        articul = soup.find_all('div', class_='sostav-item-artikul-wr')
        for art in articul:
            art = art.find('span').text.strip()
            #print(art)
    except:
        art = 'null'

    try:
        size = soup.find_all('div', class_='sostav-item-color-wr')
        for ss in size:
            ss = ss.find('span').text.strip().replace('\n', '').replace('																								', '')
            #print(ss)
    except:
        ss = 'null'


    price1 = soup.find_all('div', class_='sostav-item-price-wr')
    for pr1 in price1:
        try:
            pr1 = pr1.find('span', class_='pp').find('span').text.strip().replace('\t', '').replace('\n', '')
            #print(pr1)
        except:
            pr1 = None

    price2 = soup.find_all('div', class_='sostav-item-price-wr')
    for pr2 in price2:
        try:
            pr2 = pr2.find('span', class_='dop_price').find('span').text.strip().replace('\t', '').replace('\n', '')
            #print(pr2)
        except:
            pr2 = None

    stats = soup.find_all('div', class_='sostav-item-color-wr')
    l_stats = []
    for stat in stats:
        stat1 = stat.text.strip().replace('\t', '').replace('\n', '')
        stat2 = stat.find('span').text.strip().replace('\t', '').replace('\n', '')
        stx = {stat1: stat2}
        l_stats.append(stx)
        #print(stx)
    current_stats = redactor_info(l_stats)


    try:
        pic = 'https://www.artpole.ru' + soup.find('a', class_='fancy_img').get('href')
        #print(pic)
    except:
        pic = 'null'

    l_download = []
    try:
        download = soup.find('div', class_='materials').find_all('div', class_='instr-item')
        for down in download:
            n = down.find('a').text.strip()
            f = 'https://www.artpole.ru' + down.find('a').get('href')
            info = {n: f}
            #print(info)
            l_download.append(info)

    except:
        info = 'null'
        l_download.append(info)
    current_download = redactor_info(l_download)

    data = {
        'name': na,
        'id': art,
        'size': ss,
        'price_1': int(pr1.replace(' ', '')),
        'price_2': int(pr1.replace(' ', '').replace(' ', '').replace('руб./кв.м', '')),
        'stats': ''.join(current_stats),
        'url_pic': pic,
        'final_info': ''.join(current_download)
    }


    today_time = str(datetime.date.today())
    db_stats = ''.join(current_stats)
    db_info = ''.join(current_download)


    print(data)
    connect_to_database(art, na, ss, pr1, pr2, db_stats, db_info, pic, today_time)
    #csv_writer(data)



def main():
    headers = h
    #url = 'https://www.artpole.ru'
    #get_list(get_html(url, headers))
    '''
    for url in LXM_list:
        print(url)
        get_list_cards(get_html(url, headers))
    '''
    error_url = []
    with open('artpole_url_list.txt', 'r') as fx:
        for line in fx.readlines():
            try:
                print(line.replace('\n', ''))
                get_data(get_html(line.replace('\n', ''), headers))
                print('------------')
                sleep(0.5)
            except:
                error_url.append(line)
                pass
    print('error url')
    for j in error_url:
        print(j)
#https://www.artpole.ru/catalog/rose_pyatyy_element_platinum.html -error
if __name__ == '__main__':
    main()