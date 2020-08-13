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
                    args.timeframe, args.exchange
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

    def get_time_frames(self):
        time_frames = []
        for key in self.exc.timeframes.keys():
            time_frames.append(key)
        return time_frames

    def get_symbols(self):
        symbols = []
        for key in self.exc.symbols:
            symbols.append(key)
        return symbols

    def get_data(self, symbol, timeframe):
        if not self.is_ohlcv_supported():
            quit()

        if not self.is_time_frame_avaliable(timeframe):
            quit()

        if not self.is_symbol_avaliable(symbol):
            quit()

        ohlcv = self.exc.fetch_ohlcv(symbol, timeframe)
        columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df = pd.DataFrame(data=ohlcv, columns=columns)  # .set_index("Date")
        df["Date"] = pd.to_datetime(df["Date"], unit="ms", origin="unix")
        return df
