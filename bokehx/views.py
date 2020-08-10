from django.shortcuts import render

# Create your views here.
# for bokeh
import bokeh
from bokeh.models import ColumnDataSource, HoverTool,  SaveTool, WheelPanTool, WheelZoomTool, BoxZoomTool, ResetTool
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.embed import components

import pandas as pd
from math import pi
import datetime
from .utils import get_data, convert_to_df, update_data
from .enums import ApiFunction, ApiInterval


from django.http import HttpResponse
from bokeh.client import pull_session
from bokeh.embed import server_session
from bokeh.util import session_id


def bokeh_client(request):
    bokehServerUrl = 'http://localhost:5006/bokeh_server'

    script = server_session(model=None,
                            session_id=session_id.generate_session_id(),
                            url=bokehServerUrl,
                            )
    context = {
        'script': script
    }
    return render(request, template_name='bokeh/client.html', context=context)


def bokeh_index(request):
    interval = ApiInterval.Min60
    apifunc = ApiFunction.DAILY
    # We use get_data method from utils
    result = get_data('EUR', 'USD', 'BE0O5L3P9EXTSH5D', interval, apifunc)

    source = convert_to_df(result)

    increasing = source.close > source.open
    decreasing = source.open > source.close
    # w = 12*60*60*1000 # half day in ms
    w = 24*60*60*1000  # 24 hours in ms

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save,hover"

    title = 'EUR to USD chart'

    # hover=HoverTool(tooltips=[
    #     ("Date", "@date"),
    #     ("Open", "@open"),
    #     ("High", "@high"),
    #     ("Low", "@low"),
    #     ("Close", "@close"),
    #     ("Volume", "@volume")
    # ])
    TOOLTIPS = [
        ("Date", "@date"),
        ("Open", "@open"),
        ("High", "@high"),
        ("Low", "$low"),
        ("Close", "@close"),
        ("Volume", "@volume")
    ]

    price_plot = figure(x_axis_type="datetime",
                        plot_width=1000, plot_height=500, title=title, tooltips=TOOLTIPS)  # tools=[SaveTool(), WheelPanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool()],

    # price_plot.add_tools(HoverTool(
    #     tooltips=[
    #         ('date',   '@date{%F}'),
    #         ('open',   '$@open{%0.2f}'),
    #         ('high',   '$@high{%0.2f}'),
    #         ('low',    '$@low{%0.2f}'),
    #         # use @{ } for field names with spaces
    #         ('close',  '$@{adj close}{%0.2f}'),
    #         ('volume', '@volume{0.00 a}'),
    #     ],

    #     formatters={
    #         'date': 'datetime',  # use 'datetime' formatter for 'date' field
    #         'close': 'printf',   # use 'printf' formatter for 'close' field
    #         # use default 'numeral' formatter for other fields
    #     },

    #     # display a tooltip whenever the cursor is vertically in line with a glyph
    #     mode='vline'
    # ))

    price_plot.background_fill_color = "#f5f5f5"
    price_plot.grid.grid_line_color = "white"
    price_plot.xaxis.axis_label = "Price"
    price_plot.yaxis.axis_label = "Date"
    price_plot.title.text = "Real Time Price: EUR/USD"

    # price_plot.xaxis.major_label_orientation = pi / 5
    price_plot.grid.grid_line_alpha = 0.3
    # price_plot.segment(source.date, source.high,source.date, source.low, color = "black")

    price_plot.vbar(x=source.date[increasing], width=w, top=source.open[increasing], bottom=source.close[increasing],
                    fill_color="green", line_color="black"
                    )
    price_plot.vbar(x=source.date[decreasing], width=w, top=source.open[decreasing], bottom=source.close[decreasing],
                    fill_color="red", line_color="black"
                    )

    script, div = components(price_plot)
    # show(price_plot) #opens browser and shows plot in browser
    # curdoc().add_periodic_callback(update_data, 1000)

    return render(request, 'bokeh/index.html', {'script': script, 'div': div, 'bokehversion': bokeh.__version__})
