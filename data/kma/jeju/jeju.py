import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


# 2016년 윤달 및 30분 데이터 보정
def adjust2016(data):
    var = []
    tmp = data["일시"].values
    for i in range(len(tmp)):
        if(tmp[i][-2:] == "30" or tmp[i][5:10] == "02-29"):
           var.append(i)
    return data.drop(var)

#null check 해서 값이 한개라도 존재하는 칼럼들을 리턴해줌
def nullCheck(dd):
    var = ["일시", "운형(운형약어)"]
    for i in dd:
        if(i == "지점" or i == "일시" or i == "운형(운형약어)" or i == "일사(MJ/m2)"):
            continue
        else:
            lop = dd[i].values
            for j in range(len(lop)):
                if(math.isnan(lop[j]) is False):
                    var.append(i)
                    break
    return var

# null 값이 한개라도 있는 칼럼들 반환
def columNullCheck(data):
    var = []
    for i in data:
        if(i == "지점" or i == "일시" or i == "운형(운형약어)"):
            continue
        else:
            lop = data[i].values
            for j in range(len(lop)):
                if(math.isnan(lop[j]) is True):
                    var.append(i)
                    break
    return var

# 칼럼의 none 값 일시 프린트
def printNullIndex(data, column):
    time = data["일시"].values
    arr = data[column].values
    for i in range(len(arr)):
        if(math.isnan(arr[i])):
            print("\t"+time[i])
           
            
# Null값이 10개 초과-갯수, 이하 - 일시 프린트     
def countOrPrint(data, column):
    for c in column:
        print(c)  
        arr = data[c].values
        count = 0
        for i in range(len(arr)):
            if(math.isnan(arr[i])):
                count += 1
        if count > 10:
            print("\t"+str(count)+"개")
        else:
            printNullIndex(data, c)
            
# 강수량, 일조, 적설량의 비 측정치를 0으로 바꾸어준다.
def adjustBaseNull(data):
    column = ["강수량(mm)", "일조(hr)", "적설(cm)"]
    for c in column:
        arr = data[c].values
        for i in range(len(arr)):
            if(math.isnan(arr[i])):
                arr[i] = 0;
            
    
    
# Importing the dataset
data1 = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2014.csv")
data2 = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2015.csv")
data3 = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2016.csv")
data4 = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2017.csv")

data3 = adjust2016(data3)

adjustBaseNull(data1)
adjustBaseNull(data2)
adjustBaseNull(data3)
adjustBaseNull(data4)

var1 = nullCheck(data1)
var2 = nullCheck(data2)
var3 = nullCheck(data3)
var4 = nullCheck(data4)  # 한경의 기준 칼럼!

set(var3) - set(var4)

col1 = columNullCheck(data1[var4])
col2 = columNullCheck(data2[var4])
col3 = columNullCheck(data3[var4])
col4 = columNullCheck(data4[var4])

countOrPrint(data1, col1)
countOrPrint(data2, col2)
countOrPrint(data3, col3)
countOrPrint(data4, col4)







