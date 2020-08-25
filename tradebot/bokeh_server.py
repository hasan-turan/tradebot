from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Dropdown, Select
from .models.exchange import Exchange

from .models.candle_stick_plotter import CandleStickPlotter
from .models.ema import Ema


import ccxt
from tradebot.utils.message_utils import show_info, show_error
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
import talib
tools = "pan,wheel_zoom,box_zoom,hover,reset,crosshair"


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
        self.cmb_timeframe = self.create_timeframes()
        self.cmb_symbol = self.create_symbols()
        self.title = "{} {} {}".format(self.cmb_timeframe.value,
                                       self.cmb_symbol.value, self.exchange.get_name())
        self.emas = []
        ema9 = Ema(9, "green", 2)
        self.emas.append(ema9)

        ema21 = Ema(21, "brown", 2)
        self.emas.append(ema21)

        ema50 = Ema(50, "red", 2)
        self.emas.append(ema50)

        ema100 = Ema(100, "black", 2)
        self.emas.append(ema100)

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

    def cmb_symbol_change(self, attrname, old, new):
        self.update_data()

    def cmb_timeframe_change(self, attrname, old, new):
        self.update_data()

    def update_data(self):

        df = self.exchange.get_data(
            self.cmb_symbol.value, self.cmb_timeframe.value)
        self.source.data.update(self.source.from_df(df))

        self.plotter.plot(self.source,
                          self.cmb_timeframe.value, self.emas)

    def create_document(self, doc):

        show_info(" Exchange in bokeh_server:{}".format(
            self.exchange.get_name()))

        df = self.exchange.get_data(
            self.cmb_symbol.value, self.cmb_timeframe.value)
        if(df.empty):
            show_info("Can not create document!- Data is not avaliable")
            return

        self.source.data = self.source.from_df(df)

        self.plotter = CandleStickPlotter(self.title, 1500, 600, tools)

        p_stock = self.plotter.plot(
            self.source, self.cmb_timeframe.value, emas=self.emas)

        self.cmb_timeframe = self.create_timeframes()
        self.cmb_timeframe.on_change('value', self.cmb_timeframe_change)

        self.cmb_symbol = self.create_symbols()
        self.cmb_symbol.on_change('value', self.cmb_symbol_change)

        # curdoc().add_root(column(elements))
        # curdoc().title = "Bokeh stocks historical prices"
        toolbar = row(self.cmb_symbol, self.cmb_timeframe)
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
