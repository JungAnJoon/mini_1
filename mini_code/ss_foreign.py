from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pymysql

def insert_data(table):
    conn = pymysql.connect(host="localhost", user="root", password="1234", db="mini", charset="utf8")
    cursor = conn.cursor()
    sql = """INSERT INTO ss_foreign(
            dates, reserve)
            VALUES(%s, %s)
        """
    cursor.execute(sql,table)
    conn.commit()
    conn.close()

url_1st = "https://finance.naver.com"
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get(url_1st)
sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
elem = driver.find_element_by_id("stock_items")
keyword = "삼성전자"
elem.clear()
elem.send_keys(keyword)
btn_search = driver.find_element_by_css_selector("button.snb_search_btn")
btn_search.click()
sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
sse = driver.find_element_by_css_selector("td.tit > a")
sse.click()
sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
inv_url = soup.select("a.tab4")[0]['href']

def crawling_insert(page):
    for k in range(1,page):
        url_com = url_1st+inv_url+("&page={}".format(k))
        driver.get(url_com)
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tbody = soup.find_all("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")[0]
        record_no = [3,4,5,6,7,11,12,13,14,15,19,20,21,22,23,27,28,29,30,31]
        for i in record_no:
            date_data = tbody.find_all("tr")[i]
            dates = date_data.find_all("td")[0].string
            reserve = float(date_data.find_all("td")[8].string.replace("%",""))
            arr = [dates, reserve]
            insert_data(arr)
        print("page:",k)

crawling_insert(53)
sleep(2)
driver.close()