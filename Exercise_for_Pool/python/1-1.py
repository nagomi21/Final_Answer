import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import time

def get_urls(restaurants):
    restaurant_urls = []
    for restaurant in restaurants:
        restaurant_article = restaurant.find('article', attrs = {'class':"style_wrap__RcQ_C"})
        restaurant_title = restaurant_article.find('div', attrs = {'class':"style_title___HrjW"})
        restaurant_url = restaurant_title.select('a')[0]
        restaurant_url = restaurant_url['href']
        restaurant_urls.append(restaurant_url)
    return(restaurant_urls)

def get_address(soup):
    address = soup.find('span', attrs = {'class':'region'})
    pre_list = re.findall('.+?[都道府県]', address.text)
    pre = ' '.join(s for s in pre_list)
    address = address.text.replace(pre, "")
    town = re.split('\d+' ,address)[0]
    address = address.replace(town, "")
    return(pre, town, address)

def get_info (url):
    time.sleep(3)
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    restaurants = soup.find_all('div', attrs = {'class':"style_restaurant__SeIVn"})
    restaurant_urls = get_urls(restaurants)

    for url in restaurant_urls:
        time.sleep(3)
        res = requests.get(url, headers=header)
        soup = BeautifulSoup(res.content, 'html.parser')

        name = soup.find('p', attrs = {'class':'fn org summary'})
        phone_number = soup.find('span', attrs = {'class':'number'})
        e_mail = ''
        address = get_address(soup)
        building = soup.find('span', attrs = {'class':'locality'})
        name = name.text.replace('\xa0', ' ')
        name = name.replace('\n', ' ')
        if building != None:
            building = building.text.replace('<', "")
        hp_url = ''
        ssl = ''

        datum = {}
        datum['店舗名'] = name
        datum['電話番号'] = phone_number.text
        datum['メールアドレス'] = e_mail
        datum['都道府県'] = address[0]
        datum['市区町村'] = address[1]
        datum['番地'] = address[2]
        datum['建物名'] = building
        datum['URL'] = hp_url
        datum['SSL'] = ssl
        data.append(datum)
    return (data)

data = []
result = 'https://r.gnavi.co.jp/eki/0002644/nabe/kods00145/rs/?bdgMin=2000&r=1000&sort=STATION'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
header = {'User-Agent': user_agent}
time.sleep(3)
r_res = requests.get(result, headers=header)
r_soup = BeautifulSoup(r_res.text, 'html.parser')
pages = []
page_ul = r_soup.find('ul', attrs = {'class':"style_pages__Y9bbR"})
page_li = page_ul.select('a')

for page in page_li:
    page = 'https://r.gnavi.co.jp' + page['href']
    pages.append(page)
pages = list(dict.fromkeys(pages))

for page in pages:
    data = get_info(page)

df = pd.DataFrame(data)
pd.options.display.max_colwidth = 60
df[:50].to_csv('C:\\Users\\wa753\\Exercise_for_Pool\\python\\ex1_web-scraping\\1-1.csv', encoding='utf-16', index = False)
