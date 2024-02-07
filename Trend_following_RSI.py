# coding: utf-8

import numpy as np
import pandas as pd
import talib as ta

df = pd.read_csv('https://raw.githubusercontent.com/brulint/backtesting/main/btceur-2h.csv')

# strategy
RSI = ta.RSI(df.close, timeperiod = 14)
signal_buy = RSI > 70
signal_sell = RSI < 30

# position
signal = signal_buy.astype(int) - signal_sell.astype(int)
df['position'] = signal.where(signal != 0).ffill() > 0

# returns
df['r_hodl'] = np.log( df['close'] / df['close'].shift() )
df['r_strat'] = df['position'].shift() * df['r_hodl']
df['r_fee'] = np.where(df['position'] != df['position'].shift(), 0.0025, 0)
df['r_net'] = df['r_strat'] - df['r_fee']

# cumulative
df[['R_hodl','R_strat','R_fee','R_net']] = df[['r_hodl','r_strat','r_fee','r_net']].cumsum()

# graphs
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

df['date'] = pd.to_datetime(df['time'], unit='s')
xformatter = DatetimeTickFormatter(hours="%H:%M", days="%d/%m", months="%m/%Y", years="%Y")

p1 = figure(height=325, width=800)
p1.xaxis[0].formatter = xformatter
p1.line(df['date'], df['close'])

p11 = figure(height=125, width=800, x_range=p1.x_range)
p11.xaxis[0].formatter = xformatter
p11.line(df.date, RSI)
p11.line(df.date, 70, color='green')
p11.line(df.date, 50, color='red')
p11.line(df.date, 30, color='green')

p2 = figure(height=325, width=800, x_range=p1.x_range)
p2.xaxis[0].formatter = xformatter
p2.line(df['date'], df['close'], color='gray')
p2.triangle(df['date'], df['close'].where((df['position'] == 1) & (df['position'].shift() == 0)), color='green', size=7)
p2.inverted_triangle(df['date'], df['close'].where((df['position'] == 0) & (df['position'].shift() == 1)), color='red', size=7)

p3 = figure(height=125, width=800, x_range=p1.x_range)
p3.xaxis[0].formatter = xformatter
p3.line(df.date, signal)

p31 = figure(height=125, width=800, x_range=p1.x_range)
p31.xaxis[0].formatter = xformatter
p31.line(df['date'], df['position'])

p4 = figure(height=150, width=800, x_range=p1.x_range)
p4.xaxis[0].formatter = xformatter
p4.line(df['date'], df['r_hodl'], color='lightgray')
p4.line(df['date'], df['r_strat'])
p4.line(df['date'], df['r_fee'], color='red')

p5 = figure(height=325, width=800, x_range=p1.x_range)
p5.xaxis[0].formatter = xformatter
p5.line(df['date'], df['R_hodl'], color='lightgray')
p5.line(df['date'], df['R_strat'])
p5.line(df['date'], df['R_net'], color='red')

layout = column(p1, p11, p3, p31, p2, p4, p5)
show(layout)
