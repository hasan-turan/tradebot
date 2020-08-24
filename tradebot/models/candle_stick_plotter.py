from tradebot.models.plotter import Plotter

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CDSView, HoverTool, BooleanFilter
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter
import pandas as pd

RED = Category20[7][6]
GREEN = Category20[5][4]
VBAR_WIDTH = 0.4
DATETIME_FORMAT = "%b %d %H:%M:%S"


class CandleStickPlotter(Plotter):
    def __init__(self, source, title, plot_width, plot_height, tools, time_frame, toolbar_location="above"):
        super().__init__(title, plot_width, plot_height,
                         tools, time_frame, toolbar_location)
        self.p = None
        self.source = source

    def set_x_axis_labels(self, time_frame):
        self.time_frame = time_frame
        # p.xaxis.major_label_overrides = {
        #     # i + int(source.data[x_axis][0]): date.strftime(DATETIME_FORMAT) for i, date in enumerate(pd.to_datetime(source.data["Date"]))
        #     i: date.strftime(DATETIME_FORMAT) for i, date in enumerate(pd.to_datetime(source.data["Date"]))
        # }
        lablels = {}
        for i, date in enumerate(pd.to_datetime(self.source.data["Date"])):
            print(i)
            lablels[i] = ""
            print("{} {} ".format("*", self.time_frame[-1]))
            if(self.time_frame.endswith("m")):
                lablels[i] = date.strftime("%M")

            elif(self.time_frame.endswith("h")):

                lablels[i] = date.strftime("%H")

            elif(self.time_frame.endswith("d")):
                lablels[i] = date.strftime("%d")

            elif(self.time_frame.endswith("w")):
                lablels[i] = date.strftime("%d")

            elif(self.time_frame.endswith("M")):
                lablels[i] = date.strftime("%-m %B")

        self.p.xaxis.major_label_overrides = lablels

    def plot(self):

        self.p = figure(
            plot_width=self.plot_width,
            plot_height=self.plot_height,
            tools=self.tools,
            title=self.title,
            toolbar_location=self.toolbar_location,
        )

        inc = self.source.data["Close"] > self.source.data["Open"]
        dec = self.source.data["Open"] > self.source.data["Close"]

        view_inc = CDSView(source=self.source, filters=[BooleanFilter(inc)])
        view_dec = CDSView(source=self.source, filters=[BooleanFilter(dec)])

        x_axis = "index"
        # map dataframe indices to date strings and use as label overrides

        self.set_x_axis_labels(self.time_frame)

        self.p.xaxis.bounds = (
            self.source.data[x_axis][0], self.source.data[x_axis][-1])
        self.p.segment(
            x0=x_axis,
            x1=x_axis,
            y0="Low",
            y1="High",
            color=RED,
            source=self.source,
            view=view_inc,
        )
        self.p.segment(
            x0=x_axis,
            x1=x_axis,
            y0="Low",
            y1="High",
            color=GREEN,
            source=self.source,
            view=view_dec,
        )

        self.p.vbar(
            x=x_axis,
            width=VBAR_WIDTH,
            top="Open",
            bottom="Close",
            fill_color=GREEN,
            line_color=GREEN,
            source=self.source,
            view=view_inc,
            name="price",
        )
        self.p.vbar(
            x=x_axis,
            width=VBAR_WIDTH,
            top="Open",
            bottom="Close",
            fill_color=RED,
            line_color=RED,
            source=self.source,
            view=view_dec,
            name="price",
        )

        # p.legend.location = "top_left"
        # p.legend.border_line_alpha = 0
        # p.legend.background_fill_alpha = 0
        # p.legend.click_policy = "mute"

        self.p.yaxis.formatter = NumeralTickFormatter(format="$ 0,0[.]000")
        self.p.x_range.range_padding = 0.05
        self.p.xaxis.ticker.desired_num_ticks = 40
        self.p.xaxis.major_label_orientation = 3.14 / 4

        # Select specific tool for the plot
        price_hover = self.p.select(dict(type=HoverTool))

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
        return self.p
