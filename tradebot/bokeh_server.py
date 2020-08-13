from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Dropdown, Select
from .models.exchange import Exchange
from .models.employee import Employee
from .models.candle_stick_plotter import CandleStickPlotter
import ccxt
from tradebot.utils.message_utils import show_info, show_error
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler

TOOLS = "pan,wheel_zoom,hover,reset,crosshair"
binance = ccxt.binance()
symbol = "BTC/USDT"
timeframe = "4h"


TITLE = "{} {} {}".format(timeframe, symbol, binance.name)

print("*" * 80)
print(
    "__file__={0:<35} | __name__={1:<20} | __package__={2:<20}".format(
        __file__, __name__, str(__package__)
    )
)


class BokehServer:
    def __init__(self):

        pass

    def create_symbols(self, exchange):
        symbols = exchange.get_symbols()
        cmb_symbols = Select(title="Symbols", value="BTC/USDT", options=symbols)
        return cmb_symbols

    def create_time_frames(self, exchange):
        time_frames = exchange.get_time_frames()
        cmb_time_frames = Select(title="Time Frames", value="4h", options=time_frames)
        return cmb_time_frames

    def create_document(self, doc):

        exchange = Exchange(binance)
        show_info(" Exchange in bokeh_server:{}".format(exchange.get_name()))

        stock = ColumnDataSource(
            data=dict(Date=[], Open=[], Close=[], High=[], Low=[], index=[])
        )

        df = exchange.get_data(symbol, timeframe)
        stock.data = stock.from_df(df)

        candleStickPlotter = CandleStickPlotter(TITLE, 1500, 600, TOOLS)
        p_stock = candleStickPlotter.plot(stock)

        cmb_time_frame = self.create_time_frames(exchange)
        cmb_symbols = self.create_symbols(exchange)

        # curdoc().add_root(column(elements))
        # curdoc().title = "Bokeh stocks historical prices"
        toolbar = row(cmb_symbols, cmb_time_frame)
        layout = column(toolbar, p_stock)
        doc.add_root(layout)
        doc.title = "Bokeh stocks historical prices"

    def run(self):

        server = Server({"/": self.create_document})
        server.start()
        print("*" * 35, "Server started", "*" * 35)
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()
