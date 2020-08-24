
from .models.exchange import Exchange
import ccxt
from .models.mplfinance_plotter import MplFinancePlotter
from bokeh.models import ColumnDataSource

TOOLS = "pan,wheel_zoom,hover,reset,crosshair"


class MplServer:
    exchange = None
    title = ""
    source = ColumnDataSource(
        data=dict(Date=[], Open=[], Close=[], High=[], Low=[], index=[])
    )

    def __init__(self):

        self.exchange = Exchange(ccxt.binance())

    def run(self):
        df = self.exchange.get_data("BTC/USDT", "4h", True)

        # CandleStickPlotter(self.title, 1500, 600, TOOLS)
        mpl = MplFinancePlotter(self.title, 1500, 600, TOOLS)
        mpl.plot(df)
