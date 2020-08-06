import datetime

import backtrader as bt

from backtrader_plotting import Bokeh
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])


class TestStrategy(bt.Strategy):
    params = (
        ('buydate', 21),
        ('holdtime', 6),
    )

    def next(self):
        if len(self.data) == self.p.buydate:
            self.buy(self.datas[0], size=None)

        if len(self.data) == self.p.buydate + self.p.holdtime:
            self.sell(self.datas[0], size=None)


modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = modpath + '/datas/BTC-USD-04082019-04082020.csv'

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy, buydate=3)

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2019, 8, 4),
        # Do not pass values before this date
        todate=datetime.datetime(2020, 8, 4),
        # Do not pass values after this date
        reverse=False
    )
    cerebro.adddata(data)

    cerebro.run()

    b = Bokeh(style='bar', plot_mode='single')
    cerebro.plot(b)
