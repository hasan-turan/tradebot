

print("*"*80)
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from .models.exchange import Exchange
from .models.employee import Employee
from .models.candle_stick_plotter import CandleStickPlotter
import ccxt
from tradebot.utils.message_utils import show_info,show_error

TOOLS = 'pan,wheel_zoom,hover,reset,crosshair'
binance = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '4h'


TITLE='{} {} {}'.format(timeframe,symbol,binance.name)
employee=Employee("Hasan",1)
employee.display()  
exchange=Exchange(binance)
show_info(" Exchange in bokeh_server:{}".format(exchange.get_name()))

stock = ColumnDataSource(
    data=dict(Date=[], Open=[], Close=[], High=[], Low=[],index=[]))
 
df = exchange.get_data(symbol,timeframe)
stock.data = stock.from_df(df)

candleStickPlotter=CandleStickPlotter(TITLE,1500,600,TOOLS)
p_stock=candleStickPlotter.plot(stock)

elements = list()
elements.append(p_stock)

curdoc().add_root(column(elements))
curdoc().title = 'Bokeh stocks historical prices'