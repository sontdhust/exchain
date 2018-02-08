"""
Exchain
"""

import sched
import time
from storage import (
    read_config,
    connect_database, close_database,
    select_tickers, select_previous_trade, insert_trade,
    write_log
)
from api import fetch_prices
from indicator import calculate_macd_histograms
from strategy import analyse_macd

SCHEDULER = sched.scheduler(time.time, time.sleep)

def main():
    """
    Main
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
        side = analyse_macd(
            macd_histograms[-read_config('strategy.macd.period'):],
            read_config('strategy.macd.movement_period'),
            read_config('strategy.macd.trend_strength_disparity')
        )
        price = macd_histograms[-1]['price']
        amount = 0
        trade_type = 'market'
        previous_trade = select_previous_trade(ticker['id'])
        if side != 'hold' and (previous_trade is None or previous_trade['side'] != side):
            insert_trade(ticker['id'], side, price, amount, trade_type)
            write_log(
                ticker['exchange'] + '_' + ticker['pair'],
                time.strftime('%d %H:%M:%S', time.localtime(macd_histograms[-1]['time'])) + '; '
                + side + '; '
                + str(price) + '; '
                + str(amount) + '; '
                + trade_type
            )
    SCHEDULER.enter(delay(interval), 1, trade, (interval,))

def delay(interval):
    """
    Delay
    """
    return interval - int(time.time()) % interval

if __name__ == "__main__":
    main()
