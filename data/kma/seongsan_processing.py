import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import matplotlib.pyplot as plt

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
        if(i == "지점" or i == "일시" or i == "운형(운형약어)"):
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
            
def findTimeIndex(arr, time):
    result = None
    for i in range(len(arr)):
        if arr[i] == time:
            result = i
    return result

def comparePyoLine(time, d1, d2, d3, d4, index, interval=25, title=None):
    plt.plot(time[index-interval:index+interval], d1[index-interval:index+interval], label="성산", color="red")
    plt.plot(time[index-interval:index+interval], d2[index-interval:index+interval], label="제주", color="green")
    plt.plot(time[index-interval:index+interval], d3[index-interval:index+interval], label="서귀포", color="gray")
    plt.plot(time[index-interval:index+interval], d4[index-interval-2:index+interval-2], label="표선(AWS)", color="black")
    plt.title(title)
    plt.show()
    
def compareLine(time, d1, d2, d3, index, interval=25, title=None):
    plt.plot(time[index-interval:index+interval], d1[index-interval:index+interval], label="성산", color="red")
    plt.plot(time[index-interval:index+interval], d2[index-interval:index+interval], label="제주", color="green")
    plt.plot(time[index-interval:index+interval], d3[index-interval:index+interval], label="서귀포", color="gray")
    plt.title(title)
    plt.show()
    
def adjustCloud(check):
    term = ['Sc','ScCi', 'AcCi', 'Ci', 'ScAs', 'StNs', 'CuSc', 'ScAc', 'AsCi', 'ScAcCi', 'Ac', 'ScNs', 'StAs', 'St', 'ScAsCi', 'As', 'CbStNs', 'CbScAs', 'CuCi', 'CbSc', 'CuAc', 'CuAcCi', 'CuScAc', 'CuAs', 'CuScCi', 'CuScAcCi', 'Cu']
    target = []
    ind = None
    if check in term:
        ind = term.index(check) + 1
    else:
        ind = 0
    for i in range(28):
        if i == ind:
            target.append(1)
        else:
            target.append(0)
            
    return target

# Importing the dataset
seongsan =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/processed/processed_seongsan_2014.csv")

adjustBaseNull(seongsan)

col1 = columNullCheck(seongsan)

countOrPrint(seongsan, col1)

jeju =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2014.csv")
seogyipo =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/seogyipo/seogyipo_2014.csv")
seogyipo = adjust2016(seogyipo)
pyoseon = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/pyoseon/pyoseon_2014.csv")

ptime = pyoseon["일시"].values
var = ["풍속(m/s)","풍향(16방위)","시정(10m)","지면온도(C)"]

time = seongsan["일시"].values

pvar = pyoseon.columns

windIndex1 = findTimeIndex(time, "2014-05-19 22:00") 
windIndex2 = findTimeIndex(time, "2014-12-26 13:00") 

groundTemp = findTimeIndex(time, "2014-09-15 06:00")

# 풍속에 대한 그래프
comparePyoLine(time, seongsan[var[0]].values, jeju[var[0]].values, seogyipo[var[0]].values, pyoseon[pvar[4]].values, title = "2014 wind speed 1", index=windIndex1, interval=5)
comparePyoLine(time, seongsan[var[0]].values, jeju[var[0]].values, seogyipo[var[0]].values, pyoseon[pvar[4]].values, title = "2014 wind speed 2", index=windIndex2, interval=5)

# 풍향에 대한 그래프
comparePyoLine(time, seongsan[var[1]].values, jeju[var[1]].values, seogyipo[var[1]].values, pyoseon[pvar[4]].values, title = "2014 wind speed 1", index=windIndex1, interval=5)
comparePyoLine(time, seongsan[var[1]].values, jeju[var[1]].values, seogyipo[var[1]].values, pyoseon[pvar[4]].values, title = "2014 wind speed 2", index=windIndex2, interval=5)

#지면온도 그래프
compareLine(time, seongsan[var[3]].values, jeju[var[3]].values, seogyipo[var[3]].values, title = "2014 ground temperature", index=groundTemp, interval=5)


"""
target = []

seong = seongsan.values

# 풍속, 풍향은 표선으로 채워주고, 지면온도는 제주와 서귀포의 평균값으로 해준다
for i in seong:
    arr = i
    if i[0] == "2014-05-19 22:00":
        arr[4] = pyoseon[pvar[4]].values[windIndex1-2] #풍속
        arr[5] = pyoseon[pvar[3]].values[windIndex1-2] #풍향
    if i[0] == "2014-12-26 13:00":
        arr[4] = pyoseon[pvar[4]].values[windIndex2-2] 
        arr[5] = pyoseon[pvar[3]].values[windIndex2-2]
    if i[0] == "2014-09-15 06:00":
        arr[-1] = (jeju[var[3]].values[groundTemp] + seogyipo[var[3]].values[groundTemp]) / 2
    
    target.append(i)
result = []    


for i in target:
    arr = list(i)
    adjust = adjustCloud(arr[1])
    del arr[-2]
    del arr[1]
    result.append(arr + adjust)
    
result = np.array(result)

col = list(seongsan.columns)
del col[-2]
del col[1]
col = col + ['default','Sc','ScCi', 'AcCi', 'Ci', 'ScAs', 'StNs', 'CuSc', 'ScAc', 'AsCi', 'ScAcCi', 'Ac', 'ScNs', 'StAs', 'St', 'ScAsCi', 'As', 'CbStNs', 'CbScAs', 'CuCi', 'CbSc', 'CuAc', 'CuAcCi', 'CuScAc', 'CuAs', 'CuScCi', 'CuScAcCi', 'Cu']


newDF = pd.DataFrame(data=result, columns=col)  


newDF.to_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/processed/processed_seongsan_2014.csv", sep=',', encoding='utf-8', index=False)
    
    

"""

