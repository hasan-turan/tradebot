# myapp.py


from random import random
from math import pi
from bokeh.layouts import column, row
from bokeh.models import Button, HoverTool,SaveTool,PanTool,ResetTool,CrosshairTool,BoxZoomTool,WheelZoomTool
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from enum import Enum

import pandas as pd
import requests
from bokeh.models import ColumnDataSource,DatetimeTickFormatter
import ccxt
import pandas as pd
from datetime import date, datetime
from math import radians

binance = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'


height = 15
length = 80


def get_data(exchange, symbol, timeframe):
    """Gets data from exchange and returns as dataframe"""

    print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

    # get a list of ohlcv candles
    # each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    df = pd.DataFrame.from_records(data=ohlcv,  columns=[
                                   "date", "open", "high", "low", "close", "volume"])
    df.reindex(df["date"])
    # df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S', errors='ignore')
    # df['date'] = pd.to_datetime(df['date'])
    df["date"] = pd.to_datetime(df["date"], unit="ms")
    #df["display_time"] = df["time"].dt.strftime("%m-%d-%Y %H:%M:%S.%f")
    df = df.sort_values(by=['date'])

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(float)

    df.head()
    df.info()

    print("-------------------------------------df---------------------")
    print(df)
    return df


def convert_to_df(data):
    pass


def update_data():
    pass


df = get_data(binance, symbol, timeframe)
source = ColumnDataSource(data=df)

increasing = source.data["close"] > source.data["open"]
decreasing = source.data["open"] > source.data["close"]


w = 1*60*60*1000  # 1 hour in ms
title = symbol + ' chart'
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"


tooltips = [
    ('Date', '@date{%F}'),
    ("Open", "$@open{%0.2f}"),
    ("High", "$@high{%0.2f}"),
    ("Low", "$@low{%0.2f}"),
    ('close',  '$@close{%0.2f}'),
    ("Volume", "$@volume{%0.2f}")
]
hover = HoverTool(
    tooltips=tooltips,

    formatters={
        '@date': 'datetime',  # use 'datetime' formatter for '@date' field
        '@open': 'printf',   # use 'printf' formatter for '@{adj close}' field
        '@high': 'printf',
        '@low': 'printf',
        '@close': 'printf',
        '@volume': 'printf',

    },


)


 

plot = figure( plot_width=1000, plot_height=500,
              title=title,  tools= [CrosshairTool(), hover, BoxZoomTool(), WheelZoomTool(),ResetTool(),PanTool(),SaveTool()]) #x_axis_type="datetime",
 
plot.background_fill_color = "#f5f5f5"
plot.grid.grid_line_color = "white"
plot.xaxis.axis_label = "Date"
plot.yaxis.axis_label = "Price"
plot.axis.axis_label_text_font_style = 'bold'

plot.x_range.follow = "end"
plot.x_range.range_padding = 0

# Required to format the x-axis datetime shown on the plot,
# if omitted, time in bokeh default of micro/milliseconds.
plot.xaxis.formatter=DatetimeTickFormatter(
seconds=["%Y-%m-%d %H:%M:%S"],
minsec=["%Y-%m-%d %H:%M:%S"],
minutes=["%Y-%m-%d %H:%M:%S"],
hourmin=["%Y-%m-%d %H:%M:%S"],
hours=["%Y-%m-%d %H:%M:%S"],
days=["%Y-%m-%d %H:%M:%S"],
months=["%Y-%m-%d %H:%M:%S"],
years=["%Y-%m-%d %H:%M:%S"]
)

# Angled display for better reading.
plot.xaxis.major_label_orientation=radians(45)

plot.title.text = "{} {} from {}".format(symbol, timeframe, binance.name)
plot.xaxis.major_label_orientation = pi/4
plot.grid.grid_line_alpha = 0.3

# generates candle pins
plot.segment(source.data["date"], source.data["high"],
             source.data["date"], source.data["low"], color="black")

print("------------------increasing:{}-------------------".format(len(increasing)))
print(increasing)

print("------------------decreasing:{}-------------------".format(len(decreasing)))
print(decreasing)

print(
    "------------------source.data['open']:{}-------------------".format(len(source.data["open"])))
print(source.data["open"])

print("---------------------source.data['open'][increasing]:{}----------------".format(
    len(source.data["open"][increasing])))
print(source.data["open"][increasing])

plot.vbar(x=source.data["date"][increasing], top=source.data["open"][increasing], bottom=source.data["close"][increasing],
          width=w, fill_color="#D5E1DD", line_color="black"
          )
plot.vbar(x=source.data["date"][decreasing], top=source.data["open"][decreasing], bottom=source.data["close"][decreasing],
          width=w, fill_color="#F2583E", line_color="black"
          )

# plot.line(source.data['date'],source.data['close'], color='navy', alpha=0.5)
# plot.line(x="date", y="close", line_width=2, color='#cf3c4d',alpha=0.6, legend_label=symbol, source=source)
main_row = row(plot)
curdoc().add_root(main_row)
# curdoc().add_periodic_callback(update_data, 5000)
curdoc().title = "Bokeh chart of " + symbol
