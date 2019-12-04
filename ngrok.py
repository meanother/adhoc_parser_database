from bs4 import BeautifulSoup as bs
import requests




response = requests.get('http://127.0.0.1:4040/status')
print(response.text)