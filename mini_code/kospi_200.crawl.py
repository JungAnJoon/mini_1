from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql

def insert_kospi_200(kospi_200):
    conn = pymysql.connect(host='13.125.51.132', user='root', password='gksrud', db='test', charset='utf8')
    cur = conn.cursor()
    sql = """INSERT INTO kospi200(
             dates, price)
             VALUES(%s,%s)"""
    cur.execute(sql, kospi_200)
    conn.commit()
    conn.close()

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')

for page in range(1, 186):
    dates_list = []
    price_list = []
    base_url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page={}'
    url = base_url.format(page)
    driver.get(url)
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    dates_base = soup.select('table.type_1 > tbody > tr > td.date')
    for i in range(0, 6):
        dates_base2 = dates_base[i].string
        dates_list.append(dates_base2)

    price_base = soup.select('table.type_1 > tbody > tr > td.number_1')
    for i in range(0, 24, 4):
        price_base2 = float(price_base[i].string.replace(',', ''))
        price_list.append(price_base2)

    for i in range(0, 6):
        dates_list.sort(reverse=True)
        date = dates_list[i]
        price = price_list[i]
        arr = [date, price]
        insert_kospi_200(arr)

driver.close()