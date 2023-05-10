import requests
import numpy as np
import pandas as pd
import talib as ta
from bokeh.plotting import figure,show
from bokeh.layouts import column,row

def kbt_init (pair, period):
    # download data from Cryptowatch
    url = f'https://api.cryptowat.ch/markets/kraken/{pair}/ohlc'
    ohlc = requests.get(url).json()['result'][str(period*60)]
    columns = ['time','open','high','low','close','volume','count']
    df = pd.DataFrame(ohlc, columns=columns).astype(float)
    df['close'] = df.close.replace(to_replace=0, method='ffill')
    return df

def kbt_compute (df, sig_in, sig_out):
    # position
    sig_0 = sig_in.astype(int) - sig_out.astype(int)
    sig_1 = sig_0.where(sig_0 != 0).ffill()
    df['position'] = sig_1 > 0
    # return
    r_0 = df.close / df.close.shift()
    r_strat = np.where(df.position.shift() == 1, r_0, 1)
    r_fee = np.where(df.position.shift() + df.position == 1, 1-0.0025, 1)
    # cumulative return
    df['return_0'] = np.nancumprod(r_0)
    df['return_strat'] = np.nancumprod(r_strat)
    df['return_net'] = np.nancumprod(r_strat * r_fee)
    return df

def kbt_graph (df):
    p1 = figure(height = 300)
    p1.line(df.time, df.close)
    p1.triangle(df.time, df.close.where((df.position == 1) & (df.position.shift() == 0)), color = 'green', size = 10)
    p1.inverted_triangle(df.time, df.close.where((df.position == 0) & (df.position.shift() == 1)), color = 'red', size = 10)
    # p2 =  figure(height = 100)
    # p2.line(df.time, RSI)
    # p2.line(df.time, 70, color='green')
    # p2.line(df.time, 30, color='red')
    p5 = figure(height=300)
    p5.line(df.time, df.return_0, color='lightgray')
    p5.line(df.time, df.return_strat)
    p5.line(df.time, df.return_net, color='red')
    layout = column(p1, p5)
    # layout = column(p1, p2, p5)
    show(layout)

def kbt_test ():
    df = kbt_init ('btceur', 240) # h4
    rsi = ta.RSI(df.close, timeperiod = 14)
    df = kbt_compute (df, rsi > 70, rsi < 30)
    kbt_graph (df)
    
