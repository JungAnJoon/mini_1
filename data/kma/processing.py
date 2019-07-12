#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:29:50 2019

@author: hongbeomchoe
"""
import numpy as np
import pandas as pd
import math

# raw한 기상 데이터 받아옴
data = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/raw/seongsan-2017.csv")

# 성산을 위한 데이터 칼럼들
var =['일시', '운형(운형약어)', '기온(C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)', '증기압(hPa)', '이슬점온도(C)', '현지기압(hPa)', '해면기압(hPa)', '일조(hr)', '적설(cm)', '시정(10m)', '지면온도(C)']


tmp = data[var].values

for i in range(len(tmp)):
    for j in range(len(tmp[i])):
        if(isinstance(tmp[i][j], str)):
            continue
        else:
            if(math.isnan(tmp[i][j])):
                tmp[i][j] = None
                
newOne = pd.DataFrame(data=tmp, columns=var)  


newOne.to_csv("/Users/hongbeomchoe/Desktop/capstone/data/null_processing/null-seongsan-2017.csv", sep=',', encoding='utf-8', index=False)


