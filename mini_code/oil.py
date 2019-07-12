# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:52:56 2019

@author: anjoon
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql
import urllib
from urllib.request import urlopen
#%%
def insert_data(arr):
    conn = pymysql.connect(host="localhost", user="root", password="wjddkswns1", db="mini", charset="utf8")
    cursor = conn.cursor()
    sql = """INSERT INTO oil(
            date, oil_price)
            VALUES(%s, %s)
        """
    cursor.execute(sql, arr)
    conn.commit()
    conn.close()


#%%
def oil_crawling(page):

    for i in range(1,page):
        base_url='https://finance.naver.com/marketindex/oilDailyQuote.nhn?marketindexCd=OIL_GSL&page={}'.format(i)
        driver.get(base_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        for i in range(1,8):
            soup.select("body > div > table")
            test=soup.find_all("tr")[i]
            date=test.find_all("td")[0].string.strip()
            oil_price=float(test.find_all("td")[1].string.replace(',',''))
            arr=[date,oil_price]
            insert_data(arr)
        sleep(2)
    
#%%
if __name__ == '__main__':
    driver=webdriver.Chrome(executable_path=r"C:\Users\anjoon\PycharmProjects\ex1\chromedriver.exe")#같은 폴더에 들어있다
    driver.get("https://finance.naver.com/world/sise.nhn?symbol=SPI@SPX")
    soup=BeautifulSoup(driver.page_source,'lxml')
    
    sise=driver.find_element_by_css_selector("a.tab2")
    
    sleep(2)
    oil_crawling(3)
    driver.close()
    
   

    
    
#    iframe = driver.find_element_by_xpath('//*[@id="content"]/div[2]/iframe')
#    driver.switch_to.frame(iframe)
#    sleep(2)

    
    
    

##%%
#def oil_crawling(page):
#    for i in range(1,8):
#        soup=BeautifulSoup(driver.)
#        test=soup.find_all("tr")[i]
#        date=test.find_all("td")[0].string.strip()
#        oil_price=float(test.find_all("td")[1].string.replace(',',''))
#        date_list.append(date)
#        oil_price_list.append(oil_price)
#    
#    #219페이지까지    
#    for i in range(2,4):
#        base_url='https://finance.naver.com/marketindex/oilDailyQuote.nhn?marketindexCd=OIL_GSL&page={}'.format(i)
#        driver.get(base_url)
##        soup = BeautifulSoup(driver.page_source, 'lxml')
##        table_all=soup.select("body > div > table")
##        for i in range(1,8):
##            test=soup.find_all("tr")[i]
##            date=test.find_all("td")[0].string.strip()
##            oil_price=float(test.find_all("td")[1].string.replace(',',''))
##            date_list.append(date)
##            oil_price_list.append(oil_price)
#     
#    
#        
#  
##%%
#
##    data_test=soup.find_all("tr")[0]
##    print(data_test)
##    date=soup.find_all("td")
##    price=soup.find_all("td")
#    
#    
##%%    
#    driver = webdriver.Chrome(executable_path=r"C:\Users\anjoon\PycharmProjects\ex1\chromedriver.exe")
#    driver.get("https://finance.naver.com/marketindex/oilDetail.nhn?marketindexCd=OIL_GSL#")
#    
#    soup = BeautifulSoup(driver.page_source, 'lxml')
#    
#    sleep(2) 
#    day_sise = soup.find_all("iframe", title="일별 시세")
#    day_sise_url = day_sise['src']
#    crawling(3)