from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Dropdown, Select
from .models.exchange import Exchange

from .models.candle_stick_plotter import CandleStickPlotter

import ccxt
from tradebot.utils.message_utils import show_info, show_error
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
import talib
TOOLS = "pan,wheel_zoom,hover,reset,crosshair"


class BokehServer:

    symbol = Select()
    timeframe = Select()
    exchange = None
    source = ColumnDataSource(
        data=dict(Date=[], Open=[], Close=[], High=[], Low=[], index=[])
    )
    title = ""
    plotter = None

    def __init__(self):
        self.progressing = False
        self.exchange = Exchange(ccxt.binance())
        self.timeframe = self.create_timeframes()
        self.symbol = self.create_symbols()
        self.title = "{} {} {}".format(self.timeframe.value,
                                       self.symbol.value, self.exchange.get_name())

    def create_symbols(self):

        symbols = self.exchange.get_symbols()
        cmb_symbols = Select(
            title="Symbols", value="BTC/USDT", options=symbols)
        return cmb_symbols

    def create_timeframes(self):

        timeframes = self.exchange.get_timeframes()
        cmb_time_frames = Select(
            title="Time Frames", value="4h", options=timeframes)
        return cmb_time_frames

    def symbol_change(self, attrname, old, new):
        self.update_data()

    def timeframe_change(self, attrname, old, new):
        self.update_data()

    def update_data(self):
        if self.progressing:
            show_info("Already in progress!")
        else:
            show_info("Updating data:{} {}".format(
                self.symbol.value, self.timeframe.value))
            self.progressing = True
            df = self.exchange.get_data(
                self.symbol.value, self.timeframe.value)
            self.source.data.update(self.source.from_df(df))
            self.progressing = False

            self.plotter.set_x_axis_labels(self.timeframe.value)

    def create_document(self, doc):

        show_info(" Exchange in bokeh_server:{}".format(
            self.exchange.get_name()))

        df = self.exchange.get_data(self.symbol.value, self.timeframe.value)
        if(df.empty):
            show_info("Can not create document!- Data is not avaliable")
            return

        self.source.data = self.source.from_df(df)

        self.plotter = CandleStickPlotter(
            self.source, self.title, 1500, 600, TOOLS, self.timeframe.value)
        p_stock = self.plotter.plot()

        self.timeframe = self.create_timeframes()
        self.timeframe.on_change('value', self.timeframe_change)

        self.symbol = self.create_symbols()
        self.symbol.on_change('value', self.symbol_change)

        # curdoc().add_root(column(elements))
        # curdoc().title = "Bokeh stocks historical prices"
        toolbar = row(self.symbol, self.timeframe)
        layout = column(toolbar, p_stock)
        doc.title = "Bokeh stocks historical prices"
        doc.add_periodic_callback(self.update_data, 10)
        doc.add_root(layout)

    def run(self):

        server = Server({"/": self.create_document})
        server.start()
        print("*" * 35, "Server started", "*" * 35)
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()
