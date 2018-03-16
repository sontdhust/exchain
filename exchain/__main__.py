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
from strategy import identify_side, check_reversal, investigate_side

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
        ticker_side = analyze_macd(
            calculate_macd_histograms(prices)[-read_config('analysis.macd.period'):],
            read_config('analysis.macd.monotonic_period'),
            read_config('analysis.macd.movement_period')
        )
        update_ticker(ticker['id'], ticker_side, prices[-1]['value'])
        if ticker['priority'] > 0:
            sides.append(ticker_side)
        points[ticker['id']] = {
            'last_price': prices[-1]['value'],
            'previous_pivot': previous_pivot
        }
    side = identify_side(sides, read_config('strategy.rule.consensus_threshold'))
    if side is None:
        return
    grouped_assets = group_assets(select_assets(), side)
    point_type, trade_type = investigate_side(side)
    for assets in grouped_assets:
        trades = []
        for asset in assets[1]:
            price = points[asset['ticker_id']][point_type]
            insert_trade(asset['id'], side, price, asset['amount'], trade_type)
            trades.append({
                'exchange': asset['exchange'],
                'pair': asset['pair'],
                'price': price
            })
        notify_trades(assets[0], trades, side)
    close_database()

def group_assets(assets, side):
    """
    Group assets
    """
    reversed_assets = [a for a in assets if check_reversal(
        select_previous_trade(a['id']), side
    )]
    grouped_assets = [(u, [{key: a[key] for key in [
        'id', 'ticker_id', 'exchange', 'pair', 'amount'
    ]} for a in reversed_assets if a['slack_webhook_url'] == u]) for u in set(
        [a['slack_webhook_url'] for a in reversed_assets]
    )]
    return grouped_assets

if __name__ == "__main__":
    main()
