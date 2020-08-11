# myapp.py


from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from enum import Enum

import pandas as pd
import requests
from bokeh.models import ColumnDataSource

class ApiFunction(Enum):
    INTRA_DAY = 1,
    DAILY = 2,
    WEEKLY = 3


class ApiInterval(Enum):
    Min1 = 1,
    Min5 = 5,
    Min15 = 15,
    Min30 = 30,
    Min60 = 60


interval = ApiInterval.Min5
apifunc = ApiFunction.INTRA_DAY
apiKey = "BE0O5L3P9EXTSH5D"
fromSymbol = "EUR"
toSymbol = "USD"
function = ApiFunction.INTRA_DAY

# data = ColumnDataSource(dict(date=[], open=[], high=[], low=[], close=[]))
source = ColumnDataSource(dict(date=[], open=[], high=[], low=[], close=[]))

 

def get_Url(fromSymbol, toSymbol, apiKey, interval=ApiInterval.Min1, function=ApiFunction.INTRA_DAY):
    url = "https://www.alphavantage.co/query?function="
    if(function == ApiFunction.INTRA_DAY):
        url += "TIME_SERIES_INTRADAY&interval="
        if(interval == ApiInterval.Min1):
            url += "1Min"
        elif(interval == ApiInterval.Min5):
            url += "5Min"
        elif(interval == ApiInterval.Min15):
            url += "15Min"
        elif(interval == ApiInterval.Min30):
            url += "30Min"
        elif(interval == ApiInterval.Min60):
            url += "60Min"
    elif(function == ApiFunction.DAILY):
        url += "TIME_SERIES_DAILY"
    else:
        url += "TIME_SERIES_WEEKLY"
    url = (url+'&symbol=IBM&apikey={}').format(apiKey)

    return "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&symbol=IBM&apikey=BE0O5L3P9EXTSH5D"


def get_data(fromSymbol, toSymbol, apiKey, interval=ApiInterval.Min1,   function=ApiFunction.INTRA_DAY):
    result = requests.get(
        get_Url(fromSymbol, toSymbol, apiKey, interval, function))
    tmp_data = result.json()

    text = ""
    if(function == ApiFunction.DAILY):
        text = "Daily"
    elif(function == ApiFunction.WEEKLY):
        text = "Weekly"
    else:
        if(interval == ApiInterval.Min1):
            text = "1min"
        elif(interval == ApiInterval.Min5):
            text = "5min"
        elif(interval == ApiInterval.Min15):
            text = "15min"
        elif(interval == ApiInterval.Min30):
            text = "30min"
        elif(interval == ApiInterval.Min60):
            text = "60min"
    newData = tmp_data['Time Series ({})'.format(text)]

    return newData


def convert_to_df(data):
    """Convert the result JSON in pandas dataframe"""

    df = pd.DataFrame.from_dict(data, orient='index')

    df = df.reset_index()

    # we rename columns

    df = df.rename(index=str, columns={"index": "date", "1. open": "open",
                                       "2. high": "high", "3. low": "low", "4. close": "close", "5. volume": "volume"})

    # change to datetime

    df['date'] = pd.to_datetime(df['date'])

    # sort data according to date

    df = df.sort_values(by=['date'])

    # change the datatype

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(float)

    # Checks
    df.head()
    df.info()

    return df


def update_data():
    newData = get_data(fromSymbol, toSymbol, apiKey, interval, function)
    df = convert_to_df(newData)
    source.stream(df)
    return


# We use get_data method from utils
result = get_data(fromSymbol, toSymbol, apiKey, interval, apifunc)

soruceDf = convert_to_df(result)
source = ColumnDataSource(soruceDf)

print("---------------->source.data:{}".format(source.data))


increasing = source.data["close"] > source.data["open"]
decreasing = source.data["open"] > source.data["close"]


w = 5*1000  # 5 min in ms

TOOLS = "pan, wheel_zoom, box_zoom, reset, save,hover"

title = 'EUR to USD chart'

TOOLTIPS = [
    ("Date", "@date"),
    ("Open", "@open"),
    ("High", "@high"),
    ("Low", "$low"),
    ("Close", "@close"),
    ("Volume", "@volume")
]

price_plot = figure(x_axis_type="datetime",
                    plot_width=1000, plot_height=500, title=title, tooltips=TOOLTIPS)  # tools=[SaveTool(), WheelPanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool()],

price_plot.background_fill_color = "#f5f5f5"
price_plot.grid.grid_line_color = "white"
price_plot.xaxis.axis_label = "Price"
price_plot.yaxis.axis_label = "Date"
price_plot.title.text = "Real Time Price: EUR/USD"

# price_plot.xaxis.major_label_orientation = pi / 5
price_plot.grid.grid_line_alpha = 0.3
# price_plot.segment(soruceDf.date, soruceDf.high,soruceDf.date, soruceDf.low, color = "black")

price_plot.vbar(x=source.data["date"][increasing], width=w, top=source.data["open"][increasing], bottom=source.data["close"][increasing],
                fill_color="green", line_color="black"
                )
price_plot.vbar(x=source.data["date"][decreasing], width=w, top=source.data["open"][decreasing], bottom=source.data["close"][decreasing],
                fill_color="red", line_color="black"
                )
curdoc().add_root(price_plot)
curdoc().add_periodic_callback(update_data, 5000)
curdoc().title = "Bokeh server test"
# curdoc().add_periodic_callback(update_data, 1000)
