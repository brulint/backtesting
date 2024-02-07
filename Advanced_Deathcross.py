# coding: utf-8

import requests
import numpy as np
import pandas as pd
import talib as ta

df = pd.read_csv('./btceur-2h.csv')
#df = pd.read_csv('https://raw.githubusercontent.com/brulint/backtesting/main/btceur-2h.csv')

# strategy
EMA_15 = ta.EMA(df.close, timeperiod = 15)
SMA_high_40_offset = ta.SMA(df.high, timeperiod = 50) * 1.01
SMA_low_40_offset = ta.SMA(df.low, timeperiod = 50) / 1.01

position_long = EMA_15 > SMA_high_40_offset
position_short = EMA_15 < SMA_low_40_offset
df['position'] = position_long.astype(int) - position_short.astype(int)
position_long_in = df.close.where((position == 1) & (position.shift() == 0))
position_long_out = df.close.where((position == 0) & (position.shift() == 1))
position_short_in = df.close.where((position == -1) & (position.shift() == 0))
position_short_out = df.close.where((position == 0) & (position.shift() == -1))

# returns
df['r_hodl'] = np.log( df['close'] / df['close'].shift() )
df['r_strat'] = df['position'].shift() * df['r_hodl']
df['r_fee'] = np.where(df['position'] != df['position'].shift(), 0.0025, 0)
df['r_net'] = df['r_strat'] - df['r_fee']

# cumulative
df[['R_hodl','R_strat','R_fee','R_net']] = df[['r_hodl','r_strat','r_fee','r_net']].cumsum()

# graphic
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

df['date'] = pd.to_datetime(df.time, unit='s')
xformatter = DatetimeTickFormatter(hours="%H:%M", days="%d/%m", months="%m/%Y", years="%Y")

p1 = figure(height=325, width=900)
p1.xaxis[0].formatter = xformatter
p1.line(df.date, df.close, color='gray')
p1.line(df.date, EMA_15, color='red')
p1.line(df.date, SMA_high_40_offset, color='green')
p1.line(df.date, SMA_low_40_offset, color='green')

p2 = figure(height=325, width=900, x_range=p1.x_range)
p2.xaxis[0].formatter = xformatter
p2.line(df.date, df.close, color='gray')
p2.triangle(df.date, position_long_in, color='cyan', size=7)
p2.inverted_triangle(df.date, position_long_out, color='blue', size=7)
p2.inverted_triangle(df.date, position_short_in, color='orange', size=7)
p2.triangle(df.date, position_short_out, color='red', size=7)

p3 = figure(height=125, width=900, x_range=p1.x_range)
p3.xaxis[0].formatter = xformatter
p3.line(df.date, position)

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

layout = column(p1, p2, p3, p4, p5)
show(layout)
