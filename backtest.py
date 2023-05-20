# coding: utf-8

import requests
import numpy as np
import pandas as pd
import talib as ta
from bokeh.plotting import figure,show
from bokeh.layouts import column,row

# download data from Cryptowatch
url = f'https://api.cryptowat.ch/markets/kraken/btceur/ohlc'
ohlc = requests.get(url).json()['result'][str(4*60*60)] # 4h
columns = ['time','open','high','low','close','volume','count']
df = pd.DataFrame(ohlc, columns=columns).astype(float)
df['close'] = df.close.replace(to_replace=0, method='ffill')

# df = pd.read_csv('btceur_4h.csv').astype(float)

# strategy
RSI = ta.RSI(df.close, timeperiod = 7)
SIG_buy = RSI > 70
SIG_sell = RSI < 30

# position
SIG_0 = SIG_buy.astype(int) - SIG_sell.astype(int)
POS = SIG_0.where(SIG_0 != 0).ffill()
POS_in = df.close.where((POS == 1) & (POS.shift() == -1))
POS_out = df.close.where((POS == -1) & (POS.shift() == 1))

# return
r_0 = df.close / df.close.shift()
r_strat = np.where(POS.shift() == 1, r_0, 1)
r_fee = np.where(POS.shift() + POS == 0, 1-0.0025, 1)

# cumulative return
R_0 = np.nancumprod(r_0)
R_strat = np.nancumprod(r_strat)
R_net = np.nancumprod(r_strat * r_fee)

# graphic
p1 = figure(height=325, width=750) # ,x_axis_type='datetime')
p1.line(df.time, df.close)
p1.triangle(df.time, POS_in, color='green', size=7)
p1.inverted_triangle(df.time, POS_out, color='red', size=7)
p2 =  figure(height=125, width=750)
p2.line(df.time, RSI)
p2.line(df.time, 70, color='green')
p2.line(df.time, 30, color='red')
p3_1 = figure(height=125, width=750)
p3_1.line(df.time, SIG_buy, color='green')
p3_2 = figure(height=125, width=750)
p3_2.line(df.time, SIG_sell, color='red')
p3_3 = figure(height=125, width=750)
p3_3.line(df.time, SIG_0)
p3_4 = figure(height=125, width=750)
p3_4.line(df.time, POS)
p4 = figure(height=150, width=750)
p4.line(df.time, r_0, color='lightgray')
p4.line(df.time, r_strat)
p4.line(df.time, r_fee, color='red')
p5 = figure(height=325, width=750)
p5.line(df.time, R_0, color='lightgray')
p5.line(df.time, R_strat)
p5.line(df.time, R_net, color='red')
layout = column(p1, p2, p3_1, p3_2, p3_3, p3_4, p4, p5)
show(layout)
