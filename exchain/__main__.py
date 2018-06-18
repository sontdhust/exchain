"""
Exchain
"""

from storage import (
    read_config,
    connect_database, close_database,
    select_tickers, update_ticker,
    select_assets,
    select_previous_trade, insert_trade
)
from api import fetch_prices, notify_trades, bitflyer_trade
from indicator import calculate_macd_histograms
from analysis import analyze_macd
from strategy import identify_overall_side, check_reversal

TRADE_TYPE = 'market'

def main():
    """
    Main
    """
    connect_database(read_config('storage.database.mysql'))
    sides = []
    points = {}
    for ticker in select_tickers():
        prices = fetch_prices(
            ticker['exchange'],
            ticker['pair'],
            read_config('api.data_fetcher.interval'),
            read_config('api.data_fetcher.period')
        )
        if len(prices) == 0:
            continue
        side = analyze_macd(
            calculate_macd_histograms(prices)[-read_config('analysis.macd.period'):],
            read_config('analysis.macd.monotonic_period')
        )
        update_ticker(ticker['id'], side, prices[-1]['close'])
        if ticker['priority'] > 0:
            sides.append(side)
        points[ticker['id']] = {
            'last_price': prices[-1]['close']
        }
    overall_side = identify_overall_side(sides, read_config('strategy.rule.consensus_threshold'))
    if overall_side is None or overall_side == 'hold':
        return
    trades = []
    for asset in [a for a in select_assets()]:
        previous_trade = select_previous_trade(a['id'])
        if check_reversal(previous_trade, overall_side):
            price = points[asset['ticker_id']]['last_price']
            insert_trade(asset['id'], overall_side, price, asset['amount'], TRADE_TYPE)
            if previous_trade is not None:
                trades.append({
                    'api': asset['api'],
                    'exchange': asset['exchange'],
                    'symbol': asset['symbol'],
                    'price': price,
                    'amount': asset['amount']
                })
    execute_trade(trades, overall_side, TRADE_TYPE)
    close_database()

def execute_trade(trades, overall_side, overall_type):
    """
    Execute trade
    """
    notify_trades(trades, overall_side)
    for trade in trades:
        if trade['exchange'] == 'bitflyer':
            bitflyer_trade({
                'key': trade['api']['bitflyer_api_key'],
                'secret': trade['api']['bitflyer_api_secret']
            }, trade['symbol'], overall_type, overall_side, trade['amount'])

if __name__ == "__main__":
    main()
