# coding: utf-8

import requests
import numpy as np
import pandas as pd
import talib as ta
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

def backtest (df, SIG_buy, SIG_sell):
    #position
    SIG_0 = SIG_buy.astype(int) - SIG_sell.astype(int)
    POS = SIG_0.where(SIG_0 != 0).ffill()
    POS_buy = df.close.where((POS == 1) & (POS.shift() == -1))
    POS_sell = df.close.where((POS == -1) & (POS.shift() == 1))

    # return
    r_0 = df.close / df.close.shift()
    r_strat = np.where(POS.shift() == 1, r_0, 1)
    r_fee = np.where(POS.shift() + POS == 0, 1-0.0025, 1)

    # cumulative return
    R_0 = np.nancumprod(r_0)
    R_strat = np.nancumprod(r_strat)
    R_net = np.nancumprod(r_strat * r_fee)

    # graphic
    xformatter = DatetimeTickFormatter(hours = "%H:%M", days = "%d/%m", months = "%m/%Y", years = "%Y")
    p1 = figure(height=325, width=750, x_axis_type='datetime')
    p1.line(df.date, df.close)
    p1.triangle(df.date, POS_buy, color = 'green', size = 7)
    p1.inverted_triangle(df.date, POS_sell, color = 'red', size = 7)
    p1.xaxis[0].formatter = xformatter
    #p2 = figure(height=125, width=750, x_axis_type='datetime', x_range=p1.x_range)
    #p2.line(df.date, RSI)
    #p2.line(df.date, 70, color='green')
    #p2.line(df.date, 30, color='red')
    #p2.xaxis[0].formatter = xformatter
    p3 = figure(height=125, width=750, x_axis_type='datetime', x_range=p1.x_range)
    p3.line(df.date, POS)
    #p3.line(df.date, SIG_0)
    p3.xaxis[0].formatter = xformatter
    p4 = figure(height=150, width=750, x_axis_type='datetime', x_range=p1.x_range)
    p4.line(df.date, r_0, color='lightgray')
    p4.line(df.date, r_strat)
    p4.line(df.date, r_fee, color='red')
    p4.xaxis[0].formatter = xformatter
    p5 = figure(height=325, width=750, x_axis_type='datetime', x_range=p1.x_range)
    p5.line(df.date, R_0, color='lightgray')
    p5.line(df.date, R_strat)
    p5.line(df.date, R_net, color='red')
    p5.xaxis[0].formatter = xformatter
    layout = column(p1, p3, p4, p5)
    show(layout)

df = pd.read_csv('btceur-4h.csv').astype(float)
df['date'] = pd.to_datetime(df['time'],unit='s') # si nécessaire

# strategy
RSI = ta.RSI(df.close, timeperiod = 14)
SIG_buy = (RSI.shift() < 30) & (RSI > 30)
SIG_sell = (RSI.shift() > 70) & (RSI < 70)

backtest (df, SIG_buy, SIG_sell)
