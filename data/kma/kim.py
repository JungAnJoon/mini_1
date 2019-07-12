#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 22:42:48 2019

@author: hongbeomchoe
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def adjust2016(data):
    var = []
    tmp = data["일시"].values
    for i in range(len(tmp)):
        if(tmp[i][-2:] == "30"):
           var.append(i)
    return data.drop(var)

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




dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/kimnyeong/kim_2016.csv")
ddd = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/kimnyeong/kim_2017.csv")
dataset = adjust2016(dataset)

seongsan =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/null_processing/null-seongsan-2016.csv")

seongsan = adjust2016(seongsan)

t1 = dataset["일시"].values
for i in range(len(t1)):
    t1[i] = t1[i][5:]
t2 = seongsan["일시"].values
for i in range(len(t2)):
    t2[i] = t2[i][5:]
    
t3 = ddd["일시"].values
for i in range(len(t3)):
    t3[i] = t3[i][5:]
    
    
set(t2) - set(t1)
set(t2) - set(t3)



weatherDf = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/kimnyeong/kim_2016.csv")
weatherDf = adjust2016(weatherDf)
powerDf = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/wind_power/processed/seongsan_power_1_2016.csv")
var=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

# array로 변환
weather = weatherDf.values
power = powerDf[var].values

col = weatherDf.columns
col = col.append(pd.Index(["발전량"]))




for i in power:
    for p in i:
        for j in weather:
            
        
    


