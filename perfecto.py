import requests
from bs4 import BeautifulSoup as bs
from time import sleep

def get_html(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.ok:
        print(response.text)
        return response.text


def main():
    #url = 'https://www.alcaplastcz.ru/ru/ovladaci-tlacitka-a-senzory/antivandal/m279s-1-detail'
    url = 'https://wasserkraft.ru/product414/'
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    get_html(url, headers=headers)



    #get_data(get_html(url, headers=headers))


if __name__ == '__main__':
    main()


