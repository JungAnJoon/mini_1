from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pymysql

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

sise = driver.find_element_by_css_selector(".tab2 > span")
sise.click()
sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
day_sise = soup.find_all("iframe", title="일별 시세")[0]
day_sise_url = day_sise['src']

def insert_data(samsung):
    conn = pymysql.connect(host="localhost", user="root", password="1234", db="mini", charset="utf8")
    cursor = conn.cursor()
    sql = """INSERT INTO samsung(
            dates, price, transactions)
            VALUES(%s, %s, %s)
        """
    cursor.execute(sql,samsung)
    conn.commit()
    conn.close()

def crawling_insert(page):
    for k in range(1,page):
        url_com = url_1st+day_sise_url+("&page={}".format(k))
        driver.get(url_com)
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        item_no = [2,3,4,5,10,11,12,13,14]
        for i in item_no:
            date_test = soup.find_all("tr")[i]
            dates = date_test.find_all("td")[0].string
            price = int(date_test.find_all("td")[1].string.replace(',',''))
            transactions = int(date_test.find_all("td")[6].string.replace(',',''))
            arr = [dates, price, transactions]
            insert_data(arr)
        print("page:",k)
        sleep(2)

crawling_insert(10)
driver.close()