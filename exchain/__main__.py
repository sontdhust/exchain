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
from api import fetch_prices, notify_trade
from indicator import calculate_macd_histograms
from analysis import analyze_macd
from strategy import identify_side, check_reversal

def main():
    """
    Main
    """
    connect_database(read_config('storage.database.mysql'))
    sides = []
    for ticker in select_tickers():
        prices = fetch_prices(
            ticker['exchange'],
            ticker['pair'],
            read_config('api.data_fetcher.interval'),
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
        if ticker['priority'] > 0:
            sides.append(ticker_side)
    side = identify_side(sides, read_config('strategy.rule.consensus_threshold'))
    if side is None:
        return
    trade_type = 'market'
    reversed_assets = [a for a in select_assets() if check_reversal(
        select_previous_trade(a['id']), side
    )]
    grouped_assets = [(u, [{key: a[key] for key in [
        'id', 'exchange', 'pair', 'price', 'amount'
    ]} for a in reversed_assets if a['slack_webhook_url'] == u]) for u in set(
        [a['slack_webhook_url'] for a in reversed_assets]
    )]
    for assets in grouped_assets:
        for asset in assets[1]:
            insert_trade(asset['id'], side, asset['price'], asset['amount'], trade_type)
        notify_trade(assets, side)
    close_database()

if __name__ == "__main__":
    main()
