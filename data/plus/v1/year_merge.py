import numpy as np
import pandas as pd
import os

data1 = pd.read_csv(r'seongsan_1_2014.csv')
data2 = pd.read_csv(r'./seongsan_1_2015.csv')

col = ['일시', '기온(C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)', '증기압(hPa)',
       '이슬점온도(C)', '현지기압(hPa)', '해면기압(hPa)', '일조(hr)', '적설(cm)', '지면온도(C)',
       'default', 'Sc', 'ScCi', 'AcCi', 'Ci', 'ScAs', 'StNs', 'CuSc', 'ScAc',
       'AsCi', 'ScAcCi', 'Ac', 'ScNs', 'StAs', 'St', 'ScAsCi', 'As', 'CbStNs',
       'CbScAs', 'CuCi', 'CbSc', 'CuAc', 'CuAcCi', 'CuScAc', 'CuAs', 'CuScCi',
       'CuScAcCi', 'Cu', '발전량']

d1 = data1.values
d2 = data2.values

new = []

for i in d1:
    new.append(i)
    
for i in d2:
    new.append(i)
    
    
new = np.array(new)

newData = pd.DataFrame(new, columns = col)

newData.to_csv(r'seongsan_1_2014_2015.csv')
