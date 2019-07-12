import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



    
if __name__ == "__main__":
    
    
    
    dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/seongsan_1_2014.csv")
    #dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/non_zero_seongsan_1_2014.csv")
    

    col = ['기온(C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)', '증기압(hPa)', '이슬점온도(C)', '현지기압(hPa)', '해면기압(hPa)', '일조(hr)', '적설(cm)', '지면온도(C)', '발전량']

    data = dataset[col]
    
    data.to_csv("/Users/hongbeomchoe/Desktop/capstone/untitled/seongsan_lstm.csv", sep=',', encoding='utf-8', index=False)
