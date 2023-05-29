# coding: utf-8

import numpy as np
import pandas as pd
import talib as ta

# df = pd.read_csv('btceur_4h.csv').astype(float)
df = pd.read_csv('https://raw.githubusercontent.com/brulint/backtesting/main/btceur-4h.csv')

# strategy

df['fast'] = ta.EMA(df['close'], timeperiod = 20)
df['slow'] = ta.SMA(df['close'], timeperiod = 200)

df['position'] = df['fast'] > df['slow']

# returns

df['r_hodl'] = df['close'] / df['close'].shift()
df['r_strat'] = np.where(df['position'].shift() == 1, df['r_hodl'], 1)
df['r_fee'] = np.where(df['position'] != df['position'].shift(), 1.0025, 1)
df['r_net'] = df['r_strat'] / df['r_fee']

# cumulative

df[['R_hodl','R_strat','R_fee','R_net']] = df[['r_hodl','r_strat','r_fee','r_net']].cumprod()

# graphs

from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

df['date'] = pd.to_datetime(df['time'], unit='s')
xformatter = DatetimeTickFormatter(hours="%H:%M", days="%d/%m", months="%m/%Y", years="%Y")

p1 = figure(height=325, width=800)
p1.xaxis[0].formatter = xformatter
p1.line(df['date'], df['close'])

p2 = figure(height=325, width=800, x_range=p1.x_range)
p2.xaxis[0].formatter = xformatter
p2.line(df['date'], df['close'], color='gray')
p2.line(df['date'], df['slow'], color='red')
p2.line(df['date'], df['fast'], color='green')
p2.triangle(df['date'], df['close'].where((df['position'] == 1) & (df['position'].shift() == 0)), color='green', size=7)
p2.inverted_triangle(df['date'], df['close'].where((df['position'] == 0) & (df['position'].shift() == 1)), color='red', size=7)

p3 = figure(height=125, width=800, x_range=p1.x_range)
p3.xaxis[0].formatter = xformatter
p3.line(df['date'], df['position'])

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

layout = column(p1, p2, p3, p4, p5)
show(layout)
