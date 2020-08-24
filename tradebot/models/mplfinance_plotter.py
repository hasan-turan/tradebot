import mplfinance as mpf
from tradebot.models.plotter import Plotter


class MplFinancePlotter(Plotter):
    def plot(self, source):
        mpf.plot(source, type='candle',
                 mav=(9, 21, 50, 100),  volume=True, show_nontrading=True)
