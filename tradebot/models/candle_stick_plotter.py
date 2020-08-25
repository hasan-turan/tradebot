from typing import Sequence, Tuple, List
from tradebot.models.plotter import Plotter
from tradebot.models.ema import Ema

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CDSView, HoverTool, BooleanFilter
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter
import pandas as pd
import talib as ta

RED = Category20[7][6]
GREEN = Category20[5][4]
VBAR_WIDTH = 0.4
DATETIME_FORMAT = "%b %d %H:%M:%S"


class CandleStickPlotter(Plotter):
    def __init__(self,  title, plot_width, plot_height, tools,  toolbar_location="above"):
        super().__init__(title, plot_width, plot_height,
                         tools,  toolbar_location)
        self.graph = None

    def __set_x_axis_labels(self, source, timeframe):
        # p.xaxis.major_label_overrides = {
        #     # i + int(data[x_axis][0]): date.strftime(DATETIME_FORMAT) for i, date in enumerate(pd.to_datetime(data["Date"]))
        #     i: date.strftime(DATETIME_FORMAT) for i, date in enumerate(pd.to_datetime(data["Date"]))
        # }
        lablels = {}
        for i, date in enumerate(pd.to_datetime(source.data["Date"])):
            # print(i)
            lablels[i] = ""
            # print("{} {} ".format("*", timeframe[-1]))
            if(timeframe.endswith("m")):
                lablels[i] = date.strftime("%M")

            elif(timeframe.endswith("h")):

                lablels[i] = date.strftime("%H")

            elif(timeframe.endswith("d")):
                lablels[i] = date.strftime("%d")

            elif(timeframe.endswith("w")):
                lablels[i] = date.strftime("%d")

            elif(timeframe.endswith("M")):
                lablels[i] = date.strftime("%-m %B")

        self.graph.xaxis.major_label_overrides = lablels

    def __add_ema(self, source, x_axis, ema: Ema):

        _ema = ta.EMA(source.data['Close'], timeperiod=ema.timeperiod)
        self.graph.line(x=source.data[x_axis], y=_ema,
                        line_color=ema.linecolor,
                        legend_label="Ema " + str(ema.timeperiod),
                        line_width=ema.linewidth)

    def plot(self, source, timeframe, emas: List[Ema]) -> figure:
        x_axis = "index"
        self.graph = figure(

            plot_width=self.plot_width,
            plot_height=self.plot_height,
            tools=self.tools,
            title=self.title,
            toolbar_location=self.toolbar_location,
        )

        for ema in emas:
            self.__add_ema(source, x_axis, ema)

        inc = source.data["Close"] > source.data["Open"]
        dec = source.data["Open"] > source.data["Close"]

        view_inc = CDSView(source=source, filters=[
            BooleanFilter(inc)])
        view_dec = CDSView(source=source, filters=[
            BooleanFilter(dec)])

        # map dataframe indices to date strings and use as label overrides

        self.__set_x_axis_labels(source, timeframe)

        self.graph.xaxis.bounds = (
            source.data[x_axis][0],  source.data[x_axis][-1])
        self.graph.segment(
            x0=x_axis,
            x1=x_axis,
            y0="Low",
            y1="High",
            color=RED,
            source=source,
            view=view_inc,
        )
        self.graph.segment(
            x0=x_axis,
            x1=x_axis,
            y0="Low",
            y1="High",
            color=GREEN,
            source=source,
            view=view_dec,
        )

        self.graph.vbar(
            x=x_axis,
            width=VBAR_WIDTH,
            top="Open",
            bottom="Close",
            fill_color=GREEN,
            line_color=GREEN,
            source=source,
            view=view_inc,
            name="price",
        )
        self.graph.vbar(
            x=x_axis,
            width=VBAR_WIDTH,
            top="Open",
            bottom="Close",
            fill_color=RED,
            line_color=RED,
            source=source,
            view=view_dec,
            name="price",
        )

        self.graph.yaxis.formatter = NumeralTickFormatter(format="$ 0,0[.]000")
        self.graph.x_range.range_padding = 0.05
        self.graph.xaxis.ticker.desired_num_ticks = 40
        self.graph.xaxis.major_label_orientation = 3.14 / 4

        # Select specific tool for the plot
        price_hover = self.graph.select(dict(type=HoverTool))

        # Choose, which glyphs are active by glyph name
        price_hover.names = ["price"]
        # Creating tooltips
        # ("Datetime", "@Date{%Y-%m-%d}"),
        price_hover.tooltips = [
            ("Datetime", "@Date{%b %d %H:%M:%S}"),
            ("Open", "@Open{$0,0.00}"),
            ("High", "@High{$0,0.00}"),
            ("Low", "@Low{$0,0.00}"),
            ("Close", "@Close{$0,0.00}"),
            ("Volume", "@Volume{($ 0.00 a)}"),
        ]
        price_hover.formatters = {"@Date": "datetime"}
        price_hover.mode = "vline"

        self.graph.legend.location = "top_left"
        self.graph.legend.border_line_alpha = 0
        self.graph.legend.background_fill_alpha = 0
        self.graph.legend.click_policy = "mute"

        #self.graph.grid.grid_line_alpha = 0.3
        self.graph.xaxis.axis_label = 'Date'
        self.graph.yaxis.axis_label = 'Price'
        return self.graph
