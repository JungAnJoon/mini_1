import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/seongsan_1_2014.csv")
dataset.corr()
col = ["일시","풍속(m/s)", "풍향(16방위)", "발전량"]
data = dataset[col]
data.corr()
time = data[col[0]]
speed = data[col[1]]
direction = data[col[2]]
power = data[col[-1]]

adj = []

for a, b, c, d in zip(time, speed, direction, power):
    if d!=0:
        adj.append([a, b, c, d])
        
noZero = pd.DataFrame(data=adj, columns=col)
noZero.corr()

t1 = noZero[col[0]].values
s1 = noZero[col[1]].values
d1 = noZero[col[2]].values
p1 = noZero[col[3]].values



for i in range(len(power)):
    if power[i] == max(power):
        print(time[i])

for i in range(len(speed)):
    if speed[i] == max(speed):
        print(time[i])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
regr = linear_model.LinearRegression()

regr.fit(X_train, y_train)

regr.score(X_test, y_test)


adj2 = []    

for a, b, c in zip(time, X, y):
    if c!=0:
        adj2.append([a, b, c/6])

nzeroPower = pd.DataFrame(data=adj2, columns=col)

abcd = nzeroPower["발전량"].values;

for i in range(len(abcd)):
    if abcd[i] == 0.001/6:
        print(nzeroPower["일시"].values[i])
        
for i in range(len(y)):
    if y[i] == 0.001:
        print(time[i])
        print(X[i-1])
        print(X[i])
        print(X[i+1])

for a, b, c in zip(time, X, y):
    if b==1.3:
        print(a + " " + str(b) + " " + str(c))


for i in range(1, len(time)-1):
    if (speed[i-1] + speed[i] + speed[i+1])/3 < (3.5+1.3+0.8)/3 and power[i]!=0:
        print(time[i] + " " + str(speed[i]) + " " + str(power[i]))

