import requests
from bs4 import BeautifulSoup as bs
from config import headers as h, LXM_list
import csv
from time import sleep
import pprint


def redactor_info(list):
    qw = []
    for row in list:
        for y in row:
            a = y + ' : ' + row[y] + '; '
            qw.append(a)
    return qw


def csv_writer(data):
    with open('Ready_to_Artpole.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            data['articul'],
            data['name'],
            data['pic'],
            data['path'],
            data['material'],
            data['size'],
            data['price1'],
            data['price2'],
            data['price3'],
            data['main_pics'],
            data['full_info'],
            data['downloads'],
        ))


        '''
            'articul': ax,
            'name': name,
            'pic': pic,
            'path': path,
            'material': material,
            'size': size,
            'price1': price1,
            'price2': price2,
            'price3': price3,
            'main_pics': ''.join(list_main_pic),
            'full_info': ''.join(fixed_full_info),
            'downloads': ''.join(fixed_download)
        '''


def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    if response.ok:
        #print(response.text)
        return response.text
    else:
        print(response.status_code)

'''
second_urls = []
def get_list(html):
    soup = bs(html, 'lxml')
    urls = soup.find('div', class_='left-menu').find_all('ul')
    for url in urls:
        url = 'https://www.artpole.ru' + url.find('a').get('href')
        print(url)
        second_urls.append(url)
    second_urls.pop()
    #https://www.artpole.ru/catalog/3d_steklo.html - pass
'''

def get_cards_usr(html):
    '''Ищем ссылки на отдельные (подпрофильные) карточки'''
    with open('artpole_url_list.txt', 'a') as file:
        soup = bs(html, 'lxml')
        flexes = soup.find('div', class_='content').find('div', class_='collection new-style-collention flex-tempalte').find('div', class_='flex-tempalte-tbody').find_all('div', class_='template-line two-show-element-sect')
        for flex in flexes:
            flex = 'https://www.artpole.ru' + flex.find('a').get('href')
            file.write(flex + '\n')
            #print(flex)


def get_cards_usr_ERR(html):
    '''Ищем ссылки для урлов упавших с ошибкой'''
    with open('artpole_url_list.txt', 'a') as file:
        soup = bs(html, 'lxml')
        flexes = soup.find('div', class_='content').find_all('td', class_='preview-new-td')
        for flex in flexes:
            flex = 'https://www.artpole.ru' + flex.find('a').get('href')
            file.write(flex + '\n')
            #print(flex)


def get_data(html):
    soup = bs(html, 'lxml')


    list_main_pic = []
    try:
        main_pics = soup.find('div', class_='slider-catalog').find_all('div', class_='slider-catalog-item')
        for main_pic in main_pics:
            main_pic = 'https://www.artpole.ru' + main_pic.find('img').get('src') + ', '
            list_main_pic.append(main_pic)
    except:
        main_pic = 'NULL'
        list_main_pic.append(main_pic)

    try:
        path = soup.find('div', class_='nav').text.replace('\n', ' ').replace('\t', '')
    except:
        path = 'NULL'


    #many_cards = soup.find_all('div', class_='sostav-item new-style-im431')
    #many_cards = soup.find('div', class_='sostav dN').find_all('div')
    many_cards = soup.find('div', class_='sostav dN').find_all('table', class_='sostav-coll')
    #print(many_cards)
    index = 1

    for table in many_cards:

        try:
            pic = 'https://www.artpole.ru' + table.find('a', class_='fancy_img').get('href')
        except:
            try:
                pic = 'https://www.artpole.ru' + table.find('a', class_='fancy_img_hv').get('href')
            except:
                pic = 'NULL'


        try:
            name = table.find('div', class_='sostav-item-name').text.strip()
        except:
            name = 'NULL'

        try:
            material = table.find('div', class_='sostav-item-artikul-wr').text.strip().replace('\t', '').replace('\n', '')
        except:
            material = 'NULL'



        # Артикул
        articul = soup.find_all('div', class_='sostav-item-artikul-wr')
        try:
            ax = articul[index].find('span').text.strip()
        except:
            try:
                for art in articul:
                    ax = art.find('span').text.strip()
            except:
                ax = 'NULL'



        try:
            size = table.find('div', class_='sostav-item-color-wr').text.strip().replace('\t', '').replace('\n', '')
        except:
            size = 'NULL'



        price22 = table.find_all('div', class_='sostav-item-price-wr')
        try:
            price11_0_plus = price22[0].find_all('span', class_='pp')
            #print(price11_0_plus)
            price11_0 = price11_0_plus[3].text.strip()
            price22_0 = price22[0].find('span', class_='dop_price').text.replace('(', '').replace(')', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('руб./кв.м.', ' руб./кв.м.')
        except:
            try:
                price11_0 = price22[0].find('span', class_='pp').text.strip()
                price22_0 = price22[0].find('span', class_='dop_price').text.replace('(', '').replace(')', '').replace(
                    '\t', '').replace(' ', '').replace('\n', '').replace('руб./кв.м.', ' руб./кв.м.')
            except:
                price11_0 = 'NULL'
                price22_0 = 'NULL'

        try:
            price11_1 = price22[1].find('span', class_='pp').text.strip()
            price22_1 = price22[1].find('span', class_='dop_price').text.replace('(', '').replace(')', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('руб./кв.м.', ' руб./кв.м.')
        except:
            price11_1 = 'NULL'
            price22_1 = 'NULL'


        try:
            price11_2 = price22[2].find('span', class_='pp').text.strip()
            price22_2 = price22[2].find('span', class_='dop_price').text.replace('(', '').replace(')', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('руб./кв.м.', ' руб./кв.м.')
        except:
            price11_2 = 'NULL'
            price22_2 = 'NULL'



        price1 = price11_0 + ' ;; ' + price22_0
        price2 = price11_1 + ' ;; ' + price22_1
        price3 = price11_2 + ' ;; ' + price22_2
        #full_price = {'Цена за 1шт': price1, 'Цена за 1 кв/м': price2}
        #print(full_price)


        list_information = []
        try:
            full_information = table.find_all('div', class_='sostav-item-color-wr')
            for info in full_information:
                stat1 = info.text.strip().replace('\t', '').replace('\n', '')
                stat2 = info.find('span').text.strip().replace('\t', '').replace('\n', '')
                stx = {stat1: stat2}
                list_information.append(stx)
            fixed_full_info = redactor_info(list_information)
        except:
            stx = 'NULL'
            list_information.append(stx)
            fixed_full_info = redactor_info(list_information)


        '''Отдельный блок загрузок'''
        list_download = []
        try:
            download = soup.find('div', class_='materials').find_all('div', class_='instr-item')
            for down in download:
                n = down.find('a').text.strip()
                f = 'https://www.artpole.ru' + down.find('a').get('href')
                info = {n: f}
                list_download.append(info)
            fixed_download = redactor_info(list_download)
        except:
            info = 'NULL'
            list_download.append(info)
            fixed_download = redactor_info(list_download)


        schema = soup.find()


        data = {
            'articul': ax,
            'name': name,
            'pic': pic,
            'path': path,
            'material': material,
            'size': size,
            'price1': price1,
            'price2': price2,
            'price3': price3,
            'main_pics': ''.join(list_main_pic),
            'full_info': ''.join(fixed_full_info),
            'downloads': ''.join(fixed_download)
        }
        #pprint.pprint(data)
        if name == 'NULL':
            pass
        else:
            csv_writer(data)
            #pprint.pprint(data)
            print(data)

        index = index + 2


def main():
    headers = h
    #url = 'https://www.artpole.ru'
    err = []
    #   Наполняем список урлов для отельных карточек

    #url #1
    #https://www.artpole.ru/catalog/pallada.html

    #url >1
    #https://www.artpole.ru/catalog/silk.html

    #url = 'https://www.artpole.ru/catalog/pallada.html'
    #url = 'https://www.artpole.ru/catalog/silk.html'

    #url = 'https://www.artpole.ru/catalog/potolochnaya_kompozitsiya_spk5.html'
    #url = 'https://www.artpole.ru/catalog/vector_platinum.html'
    #url = 'https://www.artpole.ru/catalog/matrix_panels.html'
    #url = 'https://www.artpole.ru/catalog/loft-beton.html'
    url = 'https://www.artpole.ru/catalog/sultan.html'
    get_data(get_html(url, headers))


    error_urls = []
    with open('artpole_url_list.txt', 'r') as file_cards:
        for line in file_cards.readlines():
            print('Goint to this url: ' + line.replace('\n', ''))
            try:
                line = line.replace('\n', '')
                get_data(get_html(line, headers))
                sleep(0.5)
            except Exception as e:
                print(e)
                print('Упало на этом урле: ' + line)
                error_urls.append(line)
                sleep(5)
                pass
        print('------------------------')
        print('Урлы упавшие с ошибкой: ')
        for j in error_urls:
            print(j)


    '''
    for url in LXM_list:
        try:
            print(url)
            get_cards_usr(get_html(url, headers))
        except Exception as e:
            try:
                sleep(0.2)
                print('block Except for err urls!')
                get_cards_usr_ERR(get_html(url, headers))
            except:
                print(e)
                err.append(url)
        sleep(0.4)
    print('printed err urls: ')
    for i in err:
        print(i)
    '''




if __name__ == '__main__':
    main()