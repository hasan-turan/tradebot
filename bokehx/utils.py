import requests
import pandas as pd
from bokeh.models import ColumnDataSource
from .enums import ApiFunction, ApiInterval


data = ColumnDataSource(dict(date=[], open=[], high=[], low=[], close=[]))


def get_Url(fromSymbol, toSymbol, apiKey, interval=ApiInterval.Min1, function=ApiFunction.INTRA_DAY):
    url = "https://www.alphavantage.co/query?function="
    if(function == ApiFunction.INTRA_DAY):
        url += "TIME_SERIES_INTRADAY&interval="+interval
    elif(function == ApiFunction.DAILY):
        url += "TIME_SERIES_DAILY"
    else:
        url += "TIME_SERIES_WEEKLY"
    url = (url+'&symbol=IBM&apikey={}').format(apiKey)
    print("-------------->url:{}".format(url))
    return url


def update_data(fromSymbol, toSymbol, apiKey, interval=ApiInterval.Min1, function=ApiFunction.INTRA_DAY):
    print("----------------update_data hit------------------")
    newData = get_data(fromSymbol, toSymbol, apiKey, interval, function)
    data.stream(dict(date=newData["date"],
                     open=newData["open"],
                     high=newData["high"],
                     low=newData["low"],
                     close=newData["close"],), 10000)
    return


def get_data(fromSymbol, toSymbol, apiKey, interval=ApiInterval.Min1,   function=ApiFunction.INTRA_DAY):
    result = requests.get(
        get_Url(fromSymbol, toSymbol, apiKey, interval, function))
    data = result.json()

    seriesIndex = 'Time Series ({})'
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
        elif(interval == ApiInterval.Min5):
            text = "15min"
        elif(interval == ApiInterval.Min5):
            text = "30min"
        elif(interval == ApiInterval.Min5):
            text = "60min"

    return data['Time Series ({})'.format(text)]


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
