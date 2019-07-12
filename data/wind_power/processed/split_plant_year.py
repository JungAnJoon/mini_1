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
rawData = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/raw/한국남부발전_성산풍력발전실적_201712.csv")

# 데이터프레임 인덱스 변
col = rawData.columns
tmpArr = list(col)
del tmpArr[31]
tmpArr.insert(8, '00')
col = pd.Index(tmpArr)

raw = rawData.values
raw1 = raw[::2]
raw2 = raw[1::2]

raw1
raw2

adjustTime(raw1, 1)
adjustTime(raw2, 2)

# 24시의 데이터를 다음날 00시로 변경하는 부분
def adjustTime(raw, index):
    arr = []
    tmp = None

    for i in raw:
        tar = i.tolist()
        last = tar[31]
        del tar[31]
        tar.insert(8, tmp)
        tmp = last
        arr.append(tar)
    
    tmp2014 = arr[:365][:]
    tmp2015 = arr[365:730][:]
    tmp2016 = arr[730:1096][:]
    tmp2017 = arr[1096:][:]
    
    pd.DataFrame(data=tmp2014, columns=col).to_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_"+str(index)+"_2014.csv", sep=',', encoding='utf-8', index=False)
    pd.DataFrame(data=tmp2015, columns=col).to_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_"+str(index)+"_2015.csv", sep=',', encoding='utf-8', index=False)
    pd.DataFrame(data=tmp2016, columns=col).to_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_"+str(index)+"_2016.csv", sep=',', encoding='utf-8', index=False)
    pd.DataFrame(data=tmp2017, columns=col).to_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_"+str(index)+"_2017.csv", sep=',', encoding='utf-8', index=False)
    