from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql

def insert_shanghai(shanghai):
    conn = pymysql.connect(host='13.125.51.132', user='root', password='gksrud', db='test', charset='utf8')
    cur = conn.cursor()
    sql = """INSERT INTO shanghai(
             dates, price)
             VALUES(%s,%s)"""
    cur.execute(sql, shanghai)
    conn.commit()
    conn.close()

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
driver.get('https://finance.naver.com/world/sise.nhn?symbol=SHS@000001')
for page in range(1, 112):
    dates_list = []
    price_list = []
    btn_page = driver.find_element_by_id('dayLink{}'.format(page))
    btn_page.click()
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    dates_base = soup.select('table.tb_status2.tb_status2_t2 > tbody > tr > td.tb_td')
    for i in range(0, 10):
        dates_base2 = dates_base[i].string
        dates_list.append(dates_base2)

    price_base = soup.select('table.tb_status2.tb_status2_t2 > tbody > tr > td.tb_td2')
    for i in range(0, 10):
        price_base2 = float(price_base[i].string.replace(',', ''))
        price_list.append(price_base2)

    for i in range(0, 10):
        dates_list.sort(reverse=True)
        dates = dates_list[i]
        price = price_list[i]
        arr = [dates, price]
        insert_shanghai(arr)

    if page % 10 == 0:
        btn_next = driver.find_element_by_class_name('next')
        btn_next.click()

driver.close()