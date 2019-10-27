import requests
from bs4 import BeautifulSoup as bs
from config import headers as h
from time import sleep


def get_html(url, h):
    session = requests.Session()
    response = session.get(url, headers=h)
    if response.ok:
        #print(response.text)
        return response.text


def get_category_list(html):
    category_list = []
    soup = bs(html, 'lxml')
    hrefs = soup.find_all('div', class_='category col-md-4 col-sm-12 col-xs-12')
    for href in hrefs:
        category_item = 'https://www.alcaplastcz.ru' + href.find('a').get('href')
        category_list.append(category_item)
    #print(category_list)
    return category_list


def get_underdir(html):
    underdir_list = []
    soup = bs(html, 'lxml')
    hrefs = soup.find_all('div', class_='category floatleft width33')
    for href in hrefs:
        undercat_item = 'https://www.alcaplastcz.ru' + href.find('a').get('href')
        #print('Ссылка категория: ' + undercat_item)
        underdir_list.append(undercat_item)
    return underdir_list


def get_final_list(html):
    with open('alcaplastcz.txt', 'a') as file:
        final_list = []
        soup = bs(html, 'lxml')
        hrefs = soup.find_all('div', class_='vm-product-descr-container-1')
        for href in hrefs:
            item = 'https://www.alcaplastcz.ru' + href.find('a').get('href')
            print('Ссылка карточка: ' + item)
            final_list.append(item)
            file.write(item + '\n')

        return final_list


def get_data(html):
    soup = bs(html, 'lxml')
    name = soup.find('h1', itemprop='name').text.strip()
    print(name)
    under_name = soup.find('h2', class_='product-short-description').text.strip()
    print(under_name)
    use_area = soup.find('div', class_='product-pouziti').find('div', class_='custom').text.replace('Область применения', 'Область применения: ')
    print(use_area)
    id = soup.find('meta', itemprop='gtin13').get('content')
    print(id)
    techlist = soup.find('td', class_='techlist').find('a').get('href')
    print(techlist)
    downloads = soup.find('table', class_='product-params2').find_all('td', class_='filename')
    print('Downloads')
    for d in downloads:
        d = d.find('a', class_='save_as').get('href')
        print(d)
    print('Pictures')
    pic = soup.find_all('figure', itemprop='associatedMedia')
    for p in pic:
        p = 'https://www.alcaplastcz.ru' + p.find('img').get('src')
        print(p)
    print('Propeties')
    properties = soup.find('div', class_='product-vlastnosti-produktu').find_all('div', class_='row')
    for prop in properties:
        prop = prop.find('div', itemprop='description').text
        print(prop)
    print('Logistic information')
    logic = soup.find('div', class_='product-logisticke-informace').find_all('div', class_='row')
    log_list = []
    for l in logic:
        try:
            x1 = l.find('div', class_='col-md-8 col-sm-8 col-xs-8').text
            x2 = l.find('div', class_='col-md-4 col-sm-4 col-xs-4').text
            x12 = {x1: x2}
            log_list.append(x12)
            print(x12)
        except:
            pass

    print('Содержание пакета')
    package = soup.find('div', class_='product-logisticke-informace').find_all('div', class_='row')
    for pac in package:
        try:
            pac = pac.find('div', class_='col-md-12 col-sm-12 col-xs-12').text.strip()
            print(pac)

        except:
            pass


    print('----\n')




    #data = {'name': name, 'id': id, 'techlist': techlist}
    #print(data)




def main():
    headers = h

    '''
    url = 'https://www.alcaplastcz.ru/ru/vyrobky'

    main_list = get_category_list(get_html(url, headers))
    for url in main_list:
        get_underdir(get_html(url, headers))
        print(get_underdir(get_html(url, headers)))

        dirlist = get_underdir(get_html(url, headers))
        for url1 in dirlist:
            get_final_list(get_html(url1, headers))
            sleep(1.2)
    '''
    with open('alcaplastcz.txt', 'r') as file:
        for line in file:
            print(line)
            get_data(get_html(line.replace('\n', ''), headers))
            sleep(0.5)



if __name__ == '__main__':
    main()
