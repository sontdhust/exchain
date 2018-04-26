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
from api import fetch_points, notify_trades
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
        prices, previous_pivot = fetch_points(
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
            'last_price': prices[-1]['close'],
            'previous_pivot': previous_pivot
        }
    overall_side = identify_overall_side(sides, read_config('strategy.rule.consensus_threshold'))
    if overall_side is None or overall_side == 'hold':
        return
    overall_side_type = investigate_side(overall_side)
    assets = [a for a in select_assets() if check_reversal(
        select_previous_trade(a['id']), overall_side
    )]
    trades = []
    for asset in assets:
        price = points[asset['ticker_id']][overall_side_type[0]]
        insert_trade(asset['id'], overall_side, price, asset['amount'], overall_side_type[1])
        trades.append({
            'api': asset['api'],
            'exchange': asset['exchange'],
            'pair': asset['pair'],
            'price': price
        })
    notify_trades(trades, overall_side)
    close_database()

if __name__ == "__main__":
    main()
