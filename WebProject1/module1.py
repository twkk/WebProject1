#導入套件
%matplotlib inline
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#專門做『技術分析』的套件
from talib import abstract

#專門抓台股的套件
import twstock

#設定爬蟲股票代號
sid = '2330'
data=twstock.Stock(sid)

#用fetch_from抓取資料，指定日期放入dataframe裡
df = pd.DataFrame(data.fetch_from(2018,1))

#設定index
df.set_index('date', inplace = True)

#--------------------------------
#計算RSV值
rsv =df['close']-df['close'].rolling(window=9).min())/(df['close'].rolling(window=9).max()-df['close'].rolling(window=9).min())*100
rsv = np.nan_to_num(rsv)
RSV=pd.DataFrame(rsv)
RSV.columns = ['RSV']
RSV.index=df['close'].index
df['RSV'] = RSV['RSV']

#--------------------------------
#創建K值
k1 = []
for a in range(8):
    a = 74.02
    k1.append(a)
k1=pd.DataFrame(k1)
k1.columns = ['K']

k2 = []
k_temp = a
for i in range(len(df)-8):
    #當日K值=前一日K值 * 2/3 + 當日RSV * 1/3
    k_temp = k_temp*2/3+df['RSV'][i+8]*(1/3)
    k2.append(k_temp)
k2=pd.DataFrame(k2)
k2.columns = ['K']

K = pd.concat([k1,k2])
K.index=df['close'].index
df['K'] = K['K']

#--------------------------------
#創建D值
d1 = []
for b in range(8):
    b = 81.58
    d1.append(b)
d1=pd.DataFrame(d1)
d1.columns = ['D']
d2 = []
d_temp = b
for j in range(len(df)-8):
    #當日D值=前一日D值 * 2/3 + 當日K值 * 1/3
    d_temp = d_temp*2/3+df['K'][j+8]*(1/3)
    d2.append(d_temp)
d2=pd.DataFrame(d2)
d2.columns = ['D']
D = pd.concat([d1,d2])
D.index=df['close'].index
df['D'] = D['D']

#--------------------------------
#畫修正後的KD值
df['K'].plot(figsize=(16, 8), label='K')
df['D'].plot(figsize=(16, 8), label='D')
plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.title('KD_modify')

#用talib的abstract畫的KD
abstract.STOCH(df).plot(figsize=(16,8))
plt.title('KD_talib')
