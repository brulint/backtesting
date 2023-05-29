# coding: utf-8
# %load backtest1.py

import requests
import numpy as np
import pandas as pd
import talib as ta

# df = pd.read_csv('btceur_4h.csv').astype(float)
pd.read_csv('https://raw.githubusercontent.com/brulint/backtesting/main/btceur-4h.csv')

# strategy

RSI = ta.RSI(df.close, timeperiod = 14)
signal_long_buy = RSI > 70
signal_long_sell = RSI < 50
signal_short_sell = RSI < 30
signal_short_buy = RSI > 50

# position
signal_long = signal_long_buy.astype(int) - signal_long_sell.astype(int)
signal_short = signal_short_sell.astype(int) - signal_short_buy.astype(int) 
position_long = signal_long.where(signal_long != 0).ffill() > 0
position_short = signal_short.where(signal_short != 0).ffill() > 0
position = position_long.astype(int) - position_short.astype(int)

position_long_in = df.close.where((position == 1) & (position.shift() == 0))
position_long_out = df.close.where((position == 0) & (position.shift() == 1))
position_short_in = df.close.where((position == -1) & (position.shift() == 0))
position_short_out = df.close.where((position == 0) & (position.shift() == -1))


# return
r_0 = df.close / df.close.shift()
r_strat = r_0 ** position.shift().fillna(0).astype(int)
r_fee = np.where(abs(position.shift() + position) == 1, 1-0.0025, 1)

# cumulative return
R_0 = np.nancumprod(r_0)
R_strat = np.nancumprod(r_strat)
R_net = np.nancumprod(r_strat * r_fee)

# graphic
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

df['date'] = pd.to_datetime(df.time, unit='s')
xformatter = DatetimeTickFormatter(hours="%H:%M", days="%d/%m", months="%m/%Y", years="%Y")

p1 = figure(height=325, width=900)
p1.xaxis[0].formatter = xformatter
p1.line(df.date, df.close)

p11 = figure(height=125, width=900, x_range=p1.x_range)
p11.xaxis[0].formatter = xformatter
p11.line(df.date, RSI)
p11.line(df.date, 70, color='green')
p11.line(df.date, 50, color='red')
p11.line(df.date, 30, color='green')

p2 = figure(height=125, width=900, x_range=p1.x_range)
p2.xaxis[0].formatter = xformatter
p2.line(df.date, position)

p3 = figure(height=325, width=900, x_range=p1.x_range)
p3.xaxis[0].formatter = xformatter
p3.line(df.date, df.close, color='gray')
p3.triangle(df.date, position_long_in, color='cyan', size=7)
p3.inverted_triangle(df.date, position_long_out, color='blue', size=7)
p3.inverted_triangle(df.date, position_short_in, color='orange', size=7)
p3.triangle(df.date, position_short_out, color='red', size=7)

p4 = figure(height=150, width=900, x_range=p1.x_range)
p4.xaxis[0].formatter = xformatter
p4.line(df.date, r_0, color='lightgray')
p4.line(df.date, r_strat)
p4.line(df.date, r_fee, color='red')

p5 = figure(height=325, width=900, x_range=p1.x_range)
p5.xaxis[0].formatter = xformatter
p5.line(df.date, R_0, color='lightgray')
p5.line(df.date, R_strat)
p5.line(df.date, R_net, color='red')

layout = column(p1, p11, p2, p3, p4, p5)
show(layout)
