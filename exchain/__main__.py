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
from api import fetch_prices, notify_trades, bitflyer_get_positions, bitflyer_send_child_order
from indicator import calculate_macd_histograms
from analysis import analyze_macd
from strategy import identify_overall_side, check_reversal, investigate_side

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
            read_config('analysis.macd.monotonic_period'),
            read_config('analysis.macd.movement_period')
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
    overall_side_type = investigate_side(overall_side)
    trades = []
    for asset in [a for a in select_assets()]:
        previous_trade = select_previous_trade(a['id'])
        if check_reversal(previous_trade, overall_side):
            price = points[asset['ticker_id']][overall_side_type[0]]
            insert_trade(asset['id'], overall_side, price, asset['amount'], overall_side_type[1])
            if previous_trade is not None:
                trades.append({
                    'api': asset['api'],
                    'exchange': asset['exchange'],
                    'symbol': asset['symbol'],
                    'price': price,
                    'amount': asset['amount']
                })
    execute_trade(trades, overall_side.split('-')[0], overall_side_type[1])
    close_database()

def execute_trade(trades, overall_side, overall_type):
    """
    Execute trade
    """
    notify_trades(trades, overall_side)
    for trade in trades:
        if trade['exchange'] == 'bitflyer':
            api = {
                'key': trade['api']['bitflyer_api_key'],
                'secret': trade['api']['bitflyer_api_secret']
            }
            symbol = trade['symbol']
            positions = bitflyer_get_positions(api, symbol)
            amount = sum([
                p['size'] for p in positions if p['side'] != overall_side.upper()
            ]) + trade['amount']
            bitflyer_send_child_order(api, symbol, overall_type, overall_side.upper(), amount)

if __name__ == "__main__":
    main()
