from tradebot.models.plotter import Plotter

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import  CDSView ,HoverTool,BooleanFilter
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter

RED = Category20[7][6]
GREEN = Category20[5][4]
VBAR_WIDTH =0.4
DATETIME_FORMAT='%b %d %H:%M:%S'
 
class CandleStickPlotter(Plotter):
    
    def plot(self,source):
        p = figure(plot_width=self.plot_width, plot_height=self.plot_height, tools=self.tools,
               title=self.title, toolbar_location=self.toolbar_location)

        inc = source.data['Close'] > source.data['Open']
        dec = source.data['Open'] > source.data['Close']

        view_inc = CDSView(source=source, filters=[BooleanFilter(inc)])
        view_dec = CDSView(source=source, filters=[BooleanFilter(dec)])

        # map dataframe indices to date strings and use as label overrides
        p.xaxis.major_label_overrides = {
            i+int(source.data['index'][0]): date.strftime(DATETIME_FORMAT) for i, date in enumerate(pd.to_datetime(source.data["Date"]))
        }
        p.xaxis.bounds = (source.data['index'][0], source.data['index'][-1])

        p.segment(x0='index', x1='index', y0='Low', y1='High', color=RED, source=source, view=view_inc)
        p.segment(x0='index', x1='index', y0='Low', y1='High', color=GREEN, source=source, view=view_dec)


        p.vbar(x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=GREEN, line_color=GREEN,
           source=source,view=view_inc, name="price")
        p.vbar(x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=RED, line_color=RED,
           source=source,view=view_dec, name="price")

        p.legend.location = "top_left"
        p.legend.border_line_alpha = 0
        p.legend.background_fill_alpha = 0
        p.legend.click_policy = "mute"

        p.yaxis.formatter = NumeralTickFormatter(format='$ 0,0[.]000')
        p.x_range.range_padding = 0.05
        p.xaxis.ticker.desired_num_ticks = 40
        p.xaxis.major_label_orientation = 3.14/4
        
        # Select specific tool for the plot
        price_hover = p.select(dict(type=HoverTool))

        # Choose, which glyphs are active by glyph name
        price_hover.names = ["price"]
        # Creating tooltips
        #("Datetime", "@Date{%Y-%m-%d}"),
        price_hover.tooltips = [("Datetime", '@Date{%b %d %H:%M:%S}'),
                                ("Open", "@Open{$0,0.00}"),
                                ("High", "@High{$0,0.00}"),
                                ("Low", "@Low{$0,0.00}"),
                                ("Close", "@Close{$0,0.00}"),
                                ("Volume", "@Volume{($ 0.00 a)}")]
        price_hover.formatters={"@Date": 'datetime'}
        price_hover.mode='vline'
        return p




