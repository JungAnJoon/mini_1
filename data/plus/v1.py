#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:29:50 2019

@author: hongbeomchoe
"""
import numpy as np
import pandas as pd
import math


def plusCSV(year, weather, power, plant):
    newOne = []
    index=0
    for i in power:
        for k in i:
            if(math.isnan(k)):
                index += 1
                continue
            newOne.append(np.append(weather[index], [k]))
            index += 1
    newOne = np.array(newOne)
    pd.DataFrame(data=newOne, columns=col).to_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/seongsan_"+str(plant)+"_" +str(year)+".csv", sep=',', encoding='utf-8', index=False)


# raw한 기상 데이터 받아옴
weatherDf = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/processed/processed_seongsan_2015.csv")
powerDf = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_2_2015.csv")
var=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

# array로 변환
weather = weatherDf.values
power = powerDf[var].values

col = weatherDf.columns
col = col.append(pd.Index(["발전량"]))

plusCSV(2015, weather, power, 2)


