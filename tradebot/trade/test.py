from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
#from strategies.teststrategy import TestStrategy
from strategies.sma import Sma

params = {
    'cash': 1000.0,
    'commision': 0.0,
    'stake': 10,
}

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(Sma)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    # os.path.join(modpath, '/datas/orcl-1995-2014.txt')
    datapath = modpath + '/datas/BTC-USD-04082019-04082020.csv'
    #datapath = modpath + '/datas/orcl-1995-2014.txt'

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    # Do not pass values before this date
    fromdate=datetime.datetime(2020, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2020, 8, 4),
    # Do not pass values after this date
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(params['cash'])

# set commision
#  0.1% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=params['commision'])

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=params['stake'])

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
