# coding: utf-8

import requests
import numpy as np
import pandas as pd
import talib as ta
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

def backtest (df):
    
    # df: date, close, SIG_buy, SIG_sell
    # df: date, close, POS
    
    #position
    if not 'POS' in df:
        SIG_0 = df.SIG_buy.astype(int) - df.SIG_sell.astype(int)
        POS = SIG_0.where(SIG_0 != 0).ffill()
        df['POS'] = POS > 0

    POS_buy = df.close.where((df.POS == 1) & (df.POS.shift() == 0))
    POS_sell = df.close.where((df.POS == 0) & (df.POS.shift() == 1))

    # return
    r_0 = df.close / df.close.shift()
    r_strat = np.where(df.POS.shift() == 1, r_0, 1)
    r_fee = np.where(df.POS.shift() + df.POS == 1, 1-0.0025, 1)

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
    p3.line(df.date, df.POS)
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
df['date'] = pd.to_datetime(df.time, unit='s') # si nécessaire

# strategy 1
#SMA_14 = ta.SMA(df.close, timeperiod = 14)
#SMA_200 = ta.SMA(df.close, timeperiod = 200)
#df['POS'] = SMA_200 < SMA_14

#strategy 2
RSI = ta.RSI(df.close, timeperiod = 14)
df['SIG_buy'] = (RSI.shift() < 30) & (RSI > 30)
df['SIG_sell'] = (RSI.shift() > 70) & (RSI < 70)

backtest (df)
