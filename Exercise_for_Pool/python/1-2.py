from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as ChromeService
import re
import pandas as pd
import time

def get_urls(restaurants):
    restaurant_urls = []
    for restaurant in restaurants:
        restaurant_article = restaurant.find_element(By.CLASS_NAME, "style_wrap__RcQ_C")
        restaurant_title = restaurant_article.find_element(By.CLASS_NAME, "style_title___HrjW")
        restaurant_url = restaurant_title.find_element(By.TAG_NAME, "a")
        restaurant_url = restaurant_url.get_attribute("href")
        restaurant_urls.append(restaurant_url)
    return(restaurant_urls)

def get_address(driver_restaurant):
    address =  driver_restaurant.find_element(By.CLASS_NAME, "region")
    pre_list = re.findall('.+?[都道府県]', address.text)
    pre = ' '.join(s for s in pre_list)
    address = address.text.replace(pre, "")
    town = re.split('\d+' ,address)[0]
    address = address.replace(town, "")
    return(pre, town, address)

def get_page(url):
    driver_page = webdriver.Chrome(service=chrome_service, options=options)
    time.sleep(3)
    driver_page.get(page)
    page_li = driver_page.find_element(By.CLASS_NAME, "style_pages__Y9bbR")
    page_li = page_li.find_elements(By.TAG_NAME, "a")
    return(page_li)

def ssl_checker(hp_url):
    if "https://" in hp_url:
        ssl = True
    else:
        ssl = False
    return(ssl)

def shaping(hp_url):
    if 'https://' in hp_url:
        hp_url = hp_url.replace ('https://', '')
    elif 'http://' in hp_url:
        hp_url = hp_url.replace ('http://', '')
    if 'www.' in hp_url:
        hp_url = hp_url.replace('www.', '')
    hp_url = hp_url.rstrip('/')
    return(hp_url)

def url_ssl(driver_restaurant):
    if len(driver_restaurant.find_elements(By.CLASS_NAME, "go-off")) > 0:
        hp_preurl = driver_restaurant.find_element(By.CLASS_NAME, "go-off")
        hp_preurl = hp_preurl.get_attribute("href")
        redirect = webdriver.Chrome(service=chrome_service, options=options)
        time.sleep(3)
        redirect.get(hp_preurl)
        hp_url = redirect.current_url
        ssl  = ssl_checker(hp_url)
        hp_url = shaping(hp_url)
        redirect.close()
    else:
        hp_url = ''
        ssl = ''
    return(hp_url, ssl)

def get_info (url):
    driver_list = webdriver.Chrome(service=chrome_service, options=options)
    time.sleep(3)
    driver_list.get(url)
    restaurants = driver_list.find_elements(By.CLASS_NAME, "style_restaurant__SeIVn")
    restaurant_urls = get_urls(restaurants)
    driver_list.close()

    for url in restaurant_urls:
        driver_restaurant = webdriver.Chrome(service=chrome_service, options=options)
        time.sleep(3)
        driver_restaurant.get(url)

        name = driver_restaurant.find_element(By.ID, "info-name")
        phone_number =  driver_restaurant.find_element(By.CLASS_NAME, "number")
        e_mail =  ''
        address = get_address(driver_restaurant)
        building =  driver_restaurant.find_elements(By.CLASS_NAME, "locality")
        def_result = url_ssl(driver_restaurant)
        hp_url = def_result[0]
        ssl = def_result[1]

        datum = {}
        datum['店舗名'] = name.text
        datum['電話番号'] = phone_number.text
        datum['メールアドレス'] = e_mail
        datum['都道府県'] = address[0]
        datum['市区町村'] = address[1]
        datum['番地'] = address[2]
        if len(building) == 0:
            datum['建物名'] = ""
        else:
            datum['建物名'] = building[0].text
        datum['URL'] = hp_url
        datum['SSL'] = ssl
        data.append(datum)
        driver_restaurant.close()
    return (data)

chromedriver = "C:\\Users\\wa753\\Exercise_for_Pool\\python\\chromedriver.exe"
chrome_service = ChromeService.Service(executable_path=chromedriver)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument('user_agent')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
page = "https://r.gnavi.co.jp/eki/0002644/nabe/kods00145/rs/?bdgMin=2000&r=1000"

driver = webdriver.Chrome(service=chrome_service, options=options)
time.sleep(3)
driver.get(page)
page_num = len(get_page(page))

data = []

for i in range(page_num-2):
    data = get_info(page)
    if i == (page_num-3):
        break
    else:
        next_page = get_page(page)
        next_page[-2].click()
        page = next_page[-2].get_attribute("href")

driver.quit()

df = pd.DataFrame(data)
pd.options.display.max_colwidth = 60
df[:50].to_csv('C:\\Users\\wa753\\Exercise_for_Pool\\python\\ex1_web-scraping\\1-2.csv', encoding='utf-16', index = False)
