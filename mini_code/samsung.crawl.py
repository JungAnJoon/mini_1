from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql

def insert_samsung(samsung):
    conn = pymysql.connect(host='localhost', user='root', password='0104', db='miniproject', charset='utf8')
    cur = conn.cursor()
    sql = """INSERT INTO samsung(
             date, price, qty)
             VALUES(%s,%s,%s)"""
    cur.execute(sql, samsung)
    conn.commit()
    conn.close()

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')

for page in range(1, 6):
# for page in range(1, 5):
    date_list = []
    price_list = []
    qty_list = []
    base_url = 'https://finance.naver.com/item/sise_day.nhn?code=005930&page={}'
    url = base_url.format(page)
    driver.get(url)
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    date_base = soup.select('table.type2 > tbody > tr > td > span.tah.p10.gray03')
    for i in range(0, 10):
        date_base2 = date_base[i].string
        date_list.append(date_base2)

    price_base = soup.select('table.type2 > tbody > tr > td > span.tah.p11')
    for i in range(0, 60, 6):
        price_base2 = int(price_base[i].string.replace(',',''))
        price_list.append(price_base2)

    qty_base = soup.select('table.type2 > tbody > tr > td > span.tah.p11')
    for i in range(5, 60, 6):
        qty_base2 = int(qty_base[i].string.replace(',',''))
        qty_list.append(qty_base2)

    for i in range(0, 10):
        date_list.sort(reverse=True)
        date = date_list[i]
        price = price_list[i]
        qty = qty_list[i]
        arr = [date, price, qty]
        insert_samsung(arr)




# print(date_list)
# print(price_list)
# print(qty_list)



