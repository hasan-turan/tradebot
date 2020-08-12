import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.io import curdoc
from bokeh.layouts import column
import numpy as np
from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool,CrosshairTool
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter
import ccxt

binance = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'

def get_data(exchange, symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe) 
    df = pd.DataFrame.from_records(data=ohlcv,  columns=[
                                   "date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"],unit='ms', origin='unix')
    return df

df=get_data(binance,symbol,timeframe)
seqs=np.arange(df.shape[0])
df["seq"]=pd.Series(seqs)


df['date']=df['date'].apply(lambda x: x.strftime('%m/%d'))


df['mid']=df.apply(lambda x:(x['open']+x['close'])/2,axis=1)
df['height']=df.apply(lambda x:abs(x['close']-x['open'] if x['close']!=x['open'] else 0.001),axis=1)

inc = df.close > df.open
dec = df.open > df.close
w=0.3

#use ColumnDataSource to pass in data for tooltips
sourceInc=ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
sourceDec=ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))

#the values for the tooltip come from ColumnDataSource
hover = HoverTool(
    tooltips=[
        ("date", "@date"),
        ("open", "@open"),
        ("close", "@close"),
        ("percent", "@changepercent"),
    ]
)

TOOLS = [CrosshairTool(), hover]
p = figure(plot_width=1500, plot_height=600, tools=TOOLS,title = "aaa")
p.xaxis.major_label_orientation = 3.14/4
p.grid.grid_line_alpha=0.3

#this is the up tail
p.segment(df.seq[inc], df.high[inc], df.seq[inc], df.low[inc], color="red")
#this is the bottom tail
p.segment(df.seq[dec], df.high[dec], df.seq[dec], df.low[dec], color="green")
#this is the candle body for the red dates
p.rect(x='date', y='mid', width=w, height='height', fill_color="red", line_color="red", source=sourceInc)
#this is the candle body for the green dates
p.rect(x='date', y='mid', width=w, height='height', fill_color="green", line_color="green", source=sourceDec)

curdoc().add_root(p)
curdoc().title = 'Bokeh stocks historical prices'