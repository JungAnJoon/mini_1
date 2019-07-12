# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:31:19 2019

@author: CPB06GameN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#%%
#vif 테스트로 서로에게 영향을 주는 변수 확인
def VIF(dataframe_x):
    col_name=list(dataframe_x.columns)
    for i in col_name:
        aaa=dataframe_x.drop(i,axis=1)#feature를 없앤다
        aaa_df=pd.DataFrame(aaa)
        reg=LinearRegression()
        reg.fit(aaa_df,dataframe_x[i]) #fit는 LinearRegression의 함수이다
        R_square=reg.score(aaa_df,dataframe_x[i])
        R_square
        print(i+':', 1/(1-R_square))

#%%
#상관관계 순으로 forward stepwise 방식으로 하나씩 넣어가면서 accuracy 확인!
def forward_stepwise(dataframe):
    cor1=dataframe.corr()
    cor2=np.abs(cor1.iloc[1:9,0])
    cor3=cor2.sort_values()
    columns=cor3.index.values
    
    new_columns=[]
    max=0
    tmp=[]
    for i in range(7,-1,-1):
        tmp.append(columns[i])
        X=dataframe.loc[:,tmp]
        y=dataframe.loc[:,'price_ss']
        reg=LinearRegression()
        reg.fit(X,y)
        accuracy=reg.score(X,y)
        if(accuracy>=max):
            max=accuracy
            new_columns.append(columns[i])
            print(tmp)
            print(accuracy)
        else:
            break;
    return accuracy,new_columns
#%%
def reg_fit(train_X,train_y):
    reg=LinearRegression()
    reg1=reg.fit(train_X,train_y)
    return reg1

#%%    
def reg_score(train_X,train_y,test_X,test_y):
    reg=reg_fit(train_X,train_y)
    score=reg.score(test_X,test_y)
    return score

#%%
def reg_predict(train_X,train_y,X):
    model=reg_fit(train_X,train_y)
    predictions = model.predict(X)
    return predictions

    
    
#%%
if __name__ == "__main__":
    df=pd.read_csv(r"C:\Users\anjoon\Desktop\mini1\dataframe_total.csv")
    df["price_ss"]=df["price_ss"]/50
    
    #2015~2018
    df1=df.loc[:968,'price_sk']
    df2=df.loc[:968,'price_ss']
    df3=df.loc[:968,['transaction_sk','oil','snp','shanghai','kospi','hold_sk','exchange','export']]
    df4=df.loc[:968,['transaction_ss','oil', 'snp', 'shanghai', 'kospi', 'hold_ss', 'exchange','export']]
    df_sk=pd.concat([df1,df3],axis=1)
    df_ss=pd.concat([df2,df4],axis=1)
    
    #sk train_set,test_set
    df_sk_x=df_sk.iloc[:,1:]
    df_sk_y=df_sk.iloc[:,0]
    X_train_sk, X_test_sk, y_train_sk, y_test_sk = train_test_split(df_sk_x, df_sk_y, test_size=0.2)
    
    #samsung train_set,test_set
    df_ss_x=df_ss.iloc[:,1:]
    df_ss_y=df_ss.iloc[:,0]
    X_train_ss, X_test_ss, y_train_ss,  y_test_ss = train_test_split(df_ss_x, df_ss_y, test_size=0.2)
    
    #model performance
    score_sk=reg_score(X_train_sk, y_train_sk, X_test_sk , y_test_sk)
    score_ss=reg_score(X_train_ss, y_train_ss, X_test_ss, y_test_ss)
    
    #2019
    df5=df.loc[969:,'price_sk']
    df6=df.loc[969:,'price_ss']
    df7=df.loc[969:,['transaction_sk','oil','snp','shanghai','kospi','hold_sk','exchange','export']]
    df8=df.loc[969:,['transaction_ss','oil', 'snp', 'shanghai', 'kospi', 'hold_ss', 'exchange','export']]
    df_sk_2019=pd.concat([df5,df7],axis=1)
    df_ss_2019=pd.concat([df6,df8],axis=1)
    
    #sk predict
    X_2019_sk=df_sk_2019.iloc[:,1:]
    y_2019_sk=df_sk_2019.iloc[:,0]
    predictions_sk=reg_predict(X_train_sk,y_train_sk,X_2019_sk)
    predictions_sk=pd.DataFrame(predictions_sk)
    df_date=pd.DataFrame(df.iloc[969:,0])
    df_date=df_date.reset_index(drop=True)
    predictions_sk=pd.concat([df_date,predictions_sk],axis=1)
    predictions_sk=predictions_sk.rename(columns={0:'price'})
    predictions_sk=predictions_sk.set_index('date')
    
    #samsung predict
    X_2019_ss=df_ss_2019.iloc[:,1:]
    y_2019_ss=df_ss_2019.iloc[:,0]
    predictions_ss=reg_predict(X_train_ss,y_train_ss,X_2019_ss)
    predictions_ss=pd.DataFrame(predictions_ss)
    df_date=pd.DataFrame(df.iloc[969:,0])
    df_date=df_date.reset_index(drop=True)
    predictions_ss=pd.concat([df_date,predictions_ss],axis=1)
    predictions_ss=predictions_ss.rename(columns={0:'price'})
    predictions_ss=predictions_ss.set_index('date')
#%%    
    #plot 
    #sk
    plt.plot(y_2019_sk, predictions_sk)
    plt.scatter(y_2019_sk, predictions_sk)
    plt.xlabel("acutal_price")
    plt.ylabel("predict_price")
    
    #samsung
    plt.plot(y_2019_ss,  predictions_ss)
    plt.scatter(y_2019_ss,  predictions_ss)
    plt.xlabel("acutal_price")
    plt.ylabel("predict_price")
    
#%%    
    #예측값 검증(RMSE)
    mse_sk = mean_squared_error(y_2019_sk, predictions_sk)
    rmse_sk = np.sqrt(mse_sk)
    
    mse_ss = mean_squared_error(y_2019_ss, predictions_ss)
    rmse_ss = np.sqrt(mse_ss)
   
 #%% 최근 일주일치 주가 예측

X_week_sk=df_sk_2019.iloc[-8:,1:]
y_week_sk=df_sk_2019.iloc[-8:,0]
predict_week_sk=reg_predict(X_train_sk,y_train_sk,X_week_sk)
predict_week_sk=pd.DataFrame(predict_week_sk)
df_tmp=df.iloc[1099:,0]
df_tmp=df_tmp.reset_index(drop=True)
predict_week_sk=pd.concat([df_tmp,predict_week_sk],axis=1)
predict_week_sk=predict_week_sk.rename(columns={0:'price'})
predict_week_sk=predict_week_sk.set_index('date')

X_week_ss=df_ss_2019.iloc[-8:,1:]
y_week_ss=df_ss_2019.iloc[-8:,0]
predict_week_ss=reg_predict(X_train_ss,y_train_ss,X_week_ss)
predict_week_ss=pd.DataFrame(predict_week_ss)
df_tmp=df.iloc[1099:,0]
df_tmp=df_tmp.reset_index(drop=True)
predict_week_ss=pd.concat([df_tmp,predict_week_ss],axis=1)
predict_week_ss=predict_week_ss.rename(columns={0:'price'})
predict_week_ss=predict_week_ss.set_index('date')

#그래프로 실제값과 예측값의 차이 확인
plt.scatter(y_week_sk,predict_week_sk)
plt.xlabel("actual price")
plt.ylabel("expected price")

plt.scatter(y_week_ss,predict_week_ss)
plt.xlabel("actual price")
plt.ylabel("expected price")








