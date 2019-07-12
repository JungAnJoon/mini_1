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
seongsan =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/null_processing/null-seongsan-2015.csv")

adjustBaseNull(seongsan)


col1 = columNullCheck(seongsan)

countOrPrint(seongsan, col1)

jeju =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/jeju/jeju_2015.csv")
seogyipo =  pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/seogyipo/seogyipo_2015.csv")
pyoseon = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/pyoseon/pyoseon_2015.csv")

time = seongsan["일시"].values
var = ["기온(C)","풍속(m/s)","풍향(16방위)","습도(%)","증기압(hPa)","이슬점온도(C)","현지기압(hPa)","해면기압(hPa)","시정(10m)","지면온도(C)"]

pvar = pyoseon.columns

"""
# 기온에 대한 그래프
comparePyoLine(time, seongsan[var[0]].values, jeju[var[0]].values, seogyipo[var[0]].values, pyoseon[pvar[2]].values, title = "2015 temperature 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)

# 풍속에 대한 그래프
comparePyoLine(time, seongsan[var[1]].values, jeju[var[1]].values, seogyipo[var[1]].values, pyoseon[pvar[4]].values, title = "2015 wind speed 1", index=findTimeIndex(time, "2015-01-26 07:00"), interval=5)
comparePyoLine(time, seongsan[var[1]].values, jeju[var[1]].values, seogyipo[var[1]].values, pyoseon[pvar[4]].values, title = "2015 wind speed 2", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)

# 풍향에 대한 그래프
comparePyoLine(time, seongsan[var[2]].values, jeju[var[2]].values, seogyipo[var[2]].values, pyoseon[pvar[3]].values, title = "2015 wind direction 1", index=findTimeIndex(time, "2015-01-26 07:00"), interval=5)
comparePyoLine(time, seongsan[var[2]].values, jeju[var[2]].values, seogyipo[var[2]].values, pyoseon[pvar[3]].values, title = "2015 wind direction 2", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)

# 습도에 대한 그래프
compareLine(time, seongsan[var[3]].values, jeju[var[3]].values, seogyipo[var[3]].values, title = "2015 humidity 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[3]].values, jeju[var[3]].values, seogyipo[var[3]].values, title = "2015 humidity 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[3]].values, jeju[var[3]].values, seogyipo[var[3]].values, title = "2015 humidity 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

# 증기압에 대한 그래프
compareLine(time, seongsan[var[4]].values, jeju[var[4]].values, seogyipo[var[4]].values, title = "2015 증기압 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[4]].values, jeju[var[4]].values, seogyipo[var[4]].values, title = "2015 증기압 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[4]].values, jeju[var[4]].values, seogyipo[var[4]].values, title = "2015 증기압 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

# 이슬점온도에 대한 그래프
compareLine(time, seongsan[var[5]].values, jeju[var[5]].values, seogyipo[var[5]].values, title = "2015 이슬점온도 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[5]].values, jeju[var[5]].values, seogyipo[var[5]].values, title = "2015 이슬점온도 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[5]].values, jeju[var[5]].values, seogyipo[var[5]].values, title = "2015 이슬점온도 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

# 현지기압에 대한 그래프
compareLine(time, seongsan[var[6]].values, jeju[var[6]].values, seogyipo[var[6]].values, title = "2015 현지기압 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[6]].values, jeju[var[6]].values, seogyipo[var[6]].values, title = "2015 현지기압 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[6]].values, jeju[var[6]].values, seogyipo[var[6]].values, title = "2015 현지기압 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

# 해면기압에 대한 그래프
compareLine(time, seongsan[var[7]].values, jeju[var[7]].values, seogyipo[var[7]].values, title = "2015 해면기압 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[7]].values, jeju[var[7]].values, seogyipo[var[7]].values, title = "2015 해면기압 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[7]].values, jeju[var[7]].values, seogyipo[var[7]].values, title = "2015 해면기압 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

#지면온도 그래프
compareLine(time, seongsan[var[-1]].values, jeju[var[-1]].values, seogyipo[var[-1]].values, title = "2015 지면온도 1", index=findTimeIndex(time, "2015-06-04 11:00"), interval=5)
compareLine(time, seongsan[var[-1]].values, jeju[var[-1]].values, seogyipo[var[-1]].values, title = "2015 지면온도 2", index=findTimeIndex(time, "2015-06-27 05:00"), interval=5)
compareLine(time, seongsan[var[-1]].values, jeju[var[-1]].values, seogyipo[var[-1]].values, title = "2015 지면온도 3", index=findTimeIndex(time, "2015-11-02 22:00"), interval=5)

"""


target = []

seong = seongsan.values

# 데이터 채워준다
for i in seong:
    arr = i
    if i[0] == "2015-01-26 07:00":
        ind = findTimeIndex(time, "2015-01-26 07:00")
        arr[4] = (jeju[var[1]].values[ind] + seogyipo[var[1]].values[ind] + pyoseon[pvar[4]].values[ind]) / 3
        arr[5] = pyoseon[pvar[3]].values[ind]
        
        
    if i[0] == "2015-06-04 11:00":
        ind = findTimeIndex(time, "2015-06-04 11:00")
        arr[2] = pyoseon[pvar[2]].values[ind]
        arr[4] = (jeju[var[1]].values[ind] + seogyipo[var[1]].values[ind] + pyoseon[pvar[4]].values[ind]) / 3
        arr[5] = pyoseon[pvar[3]].values[ind]
        arr[6] = (jeju[var[3]].values[ind] + seogyipo[var[3]].values[ind]) / 2
        arr[7] = (jeju[var[4]].values[ind] + seogyipo[var[4]].values[ind]) / 2
        arr[8] = (jeju[var[5]].values[ind] + seogyipo[var[5]].values[ind]) / 2
        arr[9] = jeju[var[6]].values[ind]
        arr[10] = (jeju[var[7]].values[ind] + seogyipo[var[7]].values[ind]) / 2
        arr[-1] = (jeju[var[-1]].values[ind] + seogyipo[var[-1]].values[ind]) / 2
        
        
    if i[0] == "2015-06-04 12:00":
        ind = findTimeIndex(time, "2015-06-04 12:00")
        arr[2] = pyoseon[pvar[2]].values[ind]
        arr[4] = (jeju[var[1]].values[ind] + seogyipo[var[1]].values[ind] + pyoseon[pvar[4]].values[ind]) / 3
        arr[5] = pyoseon[pvar[3]].values[ind]
        arr[6] = (jeju[var[3]].values[ind] + seogyipo[var[3]].values[ind]) / 2
        arr[7] = (jeju[var[4]].values[ind] + seogyipo[var[4]].values[ind]) / 2
        arr[8] = (jeju[var[5]].values[ind] + seogyipo[var[5]].values[ind]) / 2
        arr[9] = jeju[var[6]].values[ind]
        arr[10] = (jeju[var[7]].values[ind] + seogyipo[var[7]].values[ind]) / 2
        arr[-1] = (jeju[var[-1]].values[ind] + seogyipo[var[-1]].values[ind]) / 2
        
        
        
    if i[0] == "2015-06-27 05:00":
        ind = findTimeIndex(time, "2015-06-27 05:00")
        arr[6] = (seongsan[var[3]].values[ind-1] + seongsan[var[3]].values[ind+1]) / 2
        arr[7] = (seongsan[var[4]].values[ind-1] + seongsan[var[4]].values[ind+1]) / 2
        arr[8] = (seongsan[var[5]].values[ind-1] + seongsan[var[5]].values[ind+1]) / 2
        arr[9] = (seongsan[var[6]].values[ind-1] + seongsan[var[6]].values[ind+1]) / 2
        arr[10] = (seongsan[var[7]].values[ind-1] + seongsan[var[7]].values[ind+1]) / 2
        arr[-1] = (seongsan[var[-1]].values[ind-1] + seongsan[var[-1]].values[ind+1]) / 2
        
        
    if i[0] == "2015-11-02 22:00":
        ind = findTimeIndex(time, "2015-11-02 22:00")
        arr[6] = (jeju[var[3]].values[ind] + seogyipo[var[3]].values[ind]) / 2
        arr[7] = (jeju[var[4]].values[ind] + seogyipo[var[4]].values[ind]) / 2
        arr[8] = (jeju[var[5]].values[ind] + seogyipo[var[5]].values[ind]) / 2
        arr[9] = jeju[var[6]].values[ind]
        arr[10] = (jeju[var[7]].values[ind] + seogyipo[var[7]].values[ind]) / 2
        arr[-1] = (seongsan[var[-1]].values[ind-1] + seongsan[var[-1]].values[ind+1]) / 2
        
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


newDF.to_csv("/Users/hongbeomchoe/Desktop/capstone/data/kma/processed/processed_seongsan_2015.csv", sep=',', encoding='utf-8', index=False)
    