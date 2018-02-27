"""
Exchain
"""

import sched
import time
from storage import (
    read_config,
    connect_database, close_database,
    select_tickers, update_ticker,
    select_assets,
    select_previous_trade, insert_trade,
    write_log
)
from api import fetch_prices
from indicator import calculate_macd_histograms
from analysis import analyze_macd
from strategy import identify_side

SCHEDULER = sched.scheduler(time.time, time.sleep)

def main():
    """
    Main
    """
    interval = read_config('api.data_fetcher.interval')
    connect_database(read_config('storage.database.mysql'))
    SCHEDULER.enter(delay(interval), 1, execute, (interval,))
    SCHEDULER.run()
    close_database()

def execute(interval):
    """
    Execute
    """
    sides = []
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
        ticker_side = analyze_macd(
            macd_histograms[-read_config('analysis.macd.period'):],
            read_config('analysis.macd.monotonic_period'),
            read_config('analysis.macd.movement_period')
        )
        update_ticker(ticker['id'], ticker_side, prices[-1]['value'])
        sides.append(ticker_side)
    side = identify_side(sides, read_config('strategy.rule.consensus_threshold'))
    if side is None:
        return
    trade_type = 'market'
    for asset in select_assets():
        previous_trade = select_previous_trade(asset['id'])
        if side != 'hold' and (previous_trade is None or previous_trade['side'] != side):
            insert_trade(asset['id'], side, asset['price'], asset['amount'], trade_type)
            write_log(
                asset['exchange'] + '_' + asset['pair'],
                time.strftime('%d %H:%M:%S', time.localtime(prices[-1]['time'])) + '; '
                + side + '; '
                + str(asset['price']) + '; '
                + str(asset['amount']) + '; '
                + trade_type
            )
    SCHEDULER.enter(delay(interval), 1, execute, (interval,))

def delay(interval):
    """
    Delay
    """
    return interval - int(time.time()) % interval

if __name__ == "__main__":
    main()
