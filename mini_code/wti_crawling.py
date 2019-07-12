# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import keys
from time import sleep
from bs4 import BeautifulSoup
import math
import pymysql
#%%

link = "https://finance.naver.com/"     
driver=webdriver.Chrome(executable_path='chromedriver.exe")
driver.get(link)
sleep(2)
soup=Be








#%%
if __name__ == '__main__':
    link = "http://tour.interpark.com/goods/detail/?BaseGoodsCd=B3010708"
    crawling_insert(link)
