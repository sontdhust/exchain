"""
Exchain
"""

import sched
import time
from storage import read_config, connect_database, select_tickers, close_database, write_log
from api import fetch_prices
from indicator import calculate_macd_histograms
from strategy import analyse_macd

SCHEDULER = sched.scheduler(time.time, time.sleep)

def main():
    """
    Main function
    """
    interval = read_config('api.data_fetcher.interval')
    connect_database(read_config('storage.database.mysql'))
    SCHEDULER.enter(delay(interval), 1, trade, (interval,))
    SCHEDULER.run()
    close_database()

def trade(interval):
    """
    Trade
    """
    for ticker in select_tickers():
        prices = fetch_prices(
            ticker['exchange'],
            ticker['pair'],
            interval,
            read_config('api.data_fetcher.period')
        )
        if len(prices) == 0:
            continue
        macd_histograms = calculate_macd_histograms(prices)
        position = analyse_macd(
            macd_histograms[-read_config('strategy.macd.period'):],
            read_config('strategy.macd.situations')
        )
        if position != 'hold':
            write_log(
                ticker['exchange'] + '_' + ticker['pair'],
                time.strftime('%d %H:%M:%S', time.localtime(macd_histograms[-1]['time'])) + '; '
                + position + '; '
                + str(macd_histograms[-1]['price'])
            )
    SCHEDULER.enter(delay(interval), 1, trade, (interval,))

def delay(interval):
    """
    Delay
    """
    return interval - int(time.time()) % interval

if __name__ == "__main__":
    main()
