import pandas as pd
from tradebot.utils.message_utils import show_info, show_error


class Exchange:
    exc = None

    def __init__(self, exchange):
        self.exc = exchange

    def get_name(self):
        return self.exc.name

    def is_exchange_set(self):
        if self.exc == None:
            show_info("Exchange is not set!")
            return False

        return True

    def is_ohlcv_supported(self):
        if not self.is_exchange_set():
            return False

        if self.exc.has["fetchOHLCV"] != True:
            show_error(
                "{} does not support fetching OHLC data. Please use another exchange".format(
                    self.exc.name
                )
            )
            return False

        return True

    def is_time_frame_avaliable(self, timeframe):
        if not self.is_exchange_set():
            return False

        if (not hasattr(self.exc, "timeframes")) or (
            timeframe not in self.exc.timeframes
        ):
            show_error(
                "The requested timeframe ({}) is not available from {}\n".format(
                    timeframe, self.exc.name
                )
            )
            message = "Available timeframes are:\n"

            for key in self.exc.timeframes.keys():
                message += "  - " + key

            show_info(message)
            return False

        return True

    def is_symbol_avaliable(self, symbol):
        if not self.is_exchange_set():
            return False

        if self.exc.has["fetchOHLCV"] != True:
            show_info(
                "The requested symbol ({}) is not available from {}\n".format(
                    symbol, self.exc.name
                )
            )
            message = "Available symbols are:\n"
            for key in self.exc.symbols:
                message += "  - " + key
            show_info(message)
            return False

        return True

    def get_timeframes(self):
        keys = []
        for key in self.exc.timeframes.keys():
            keys.append(key)
        return keys

    def get_symbols(self):
        keys = []
        if(self.exc.symbols != None):
            for key in self.exc.symbols:
                keys.append(key)
        return keys

    def get_data(self, symbol, timeframe):
        ohlcv = []
        columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df = pd.DataFrame(data=ohlcv, columns=columns)  # .set_index("Date")
        if not self.is_ohlcv_supported():
            return df

        if not self.is_time_frame_avaliable(timeframe):
            return df

        if not self.is_symbol_avaliable(symbol):
            return df

        ohlcv = self.exc.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(data=ohlcv, columns=columns)
        df["Date"] = pd.to_datetime(df["Date"], unit="ms", origin="unix")
        return df
