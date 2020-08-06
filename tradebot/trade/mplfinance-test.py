import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import mplfinance as mpf


start = dt.datetime(2018, 1, 1)  # Start Date
end = dt.datetime.now()  # Current date as end date

Stock = web.DataReader("AAPL", "yahoo", start, end)
mpf.plot(Stock, type="candle", mav=(50, 200),
         volume=True, show_nontrading=True)
