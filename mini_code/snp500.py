from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pymysql

def insert_data(table):
    conn = pymysql.connect(host="13.125.51.132", user="root", password="gksrud", db="test", charset="utf8")
    cursor = conn.cursor()
    sql = """INSERT INTO snp500(
            dates, price)
            VALUES(%s, %s)
        """
    cursor.execute(sql,table)
    conn.commit()
    conn.close()

url = "https://finance.naver.com/"
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get(url)
sleep(2)

world = driver.find_element_by_css_selector("li.m3 > a")
world.click()
sleep(2)

snp_button = driver.find_element_by_css_selector("dt.dt3 > a")
snp_button.click()
sleep(2)

def crawling_insert(page):
    for i in range(1,page):# 페이지를 돌며
        next_page = driver.find_element_by_id("dayLink{}".format(i))
        next_page.click()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        sleep(2)
        print("---------Page:",i)
        for j in range(0, 10):# 한 행씩 긁어온다
            daily_sise = soup.find_all("tbody")[1]
            date_data = daily_sise.find_all("tr")[j]  # j는 하루치
            dates = date_data.find_all("td")[0].string
            price = float(date_data.find_all("td")[1].string.replace(",", ""))
            print(dates,price)
            arr = [dates,price]
            insert_data(arr)
        sleep(2)

        if i % 10 == 0: # 페이지 번호가 10의 배수이면 다음 버튼 클릭
            next_button = driver.find_element_by_css_selector("#dayPaging > a.next")
            next_button.click()
    sleep(2)
    driver.close()

crawling_insert(108)
