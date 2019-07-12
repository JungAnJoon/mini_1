from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql

def insert_exchange(exchange):
    conn = pymysql.connect(host='13.125.51.132', user='root', password='gksrud', db='test', charset='utf8')
    cur = conn.cursor()
    sql = """INSERT INTO exchange(
             dates, price)
             VALUES(%s,%s)"""
    cur.execute(sql, exchange)
    conn.commit()
    conn.close()

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')

for page in range(1, 113k):
    dates_list = []
    price_list = []
    base_url = 'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page={}'
    url = base_url.format(page)
    driver.get(url)
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    dates_base = soup.select('table.tbl_exchange.today > tbody > tr > td.date')
    for i in range(0, 10):
        dates_base2 = dates_base[i].string
        dates_list.append(dates_base2)

    price_base = soup.select('table.tbl_exchange.today > tbody > tr > td.num')
    for i in range(0, 20, 2):
        price_base2 = float(price_base[i].string.replace(',', ''))
        price_list.append(price_base2)

    for i in range(0, 10):
        dates_list.sort(reverse=True)
        dates = dates_list[i]
        price = price_list[i]
        arr = [dates, price]
        insert_exchange(arr)

driver.close()

