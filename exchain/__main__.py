"""
Exchain
"""

from storage import (
    read_config,
    connect_database, close_database,
    select_tickers, update_ticker,
    select_assets,
    select_previous_trade, insert_trade, select_unexecuted_trades, update_trade
)
from api import fetch_prices, notify_trades, bitflyer_trade
from indicator import calculate_macd_histograms, calculate_rsi
from analysis import analyze_macd, analyze_rsi
from strategy import decide_side, check_side_change

TRADE_TYPE = 'market'

def main():
    """
    Main
    """
    connect_database(read_config('storage.database.mysql'))
    tickers = {}
    for ticker in select_tickers():
        prices = fetch_prices(
            ticker['exchange'],
            ticker['pair'],
            read_config('api.data_fetcher.interval'),
            read_config('api.data_fetcher.period')
        )
        if len(prices) == 0:
            continue
        macd_side = analyze_macd(
            calculate_macd_histograms(prices)[-read_config('analysis.macd.period'):],
            read_config('analysis.macd.monotonic_period')
        )
        rsi_side = analyze_rsi(
            calculate_rsi(prices),
            read_config('strategy.rsi.oversold_level'),
            read_config('strategy.rsi.overbought_level')
        )
        side = None if macd_side != rsi_side else macd_side
        update_ticker(ticker['id'], side, prices[-1]['close'])
        tickers[ticker['id']] = {
            'priority': ticker['priority'],
            'side': side,
            'price': prices[-1]['close']
        }
    sides = [t['side'] for t in tickers.values() if t['priority'] > 0]
    trades = []
    for asset in select_assets():
        previous_trade = select_previous_trade(asset['id'])
        new_side = decide_side(
            sides,
            tickers[asset['ticker_id']]['side'],
            previous_trade['side'] if previous_trade is not None else None,
            read_config('strategy.rule.consensus_threshold')
        )
        if new_side is not None and check_side_change(previous_trade, new_side):
            price = tickers[asset['ticker_id']]['price']
            amount = 0 if new_side == 'hold' else asset['size']
            insert_trade(asset['id'], new_side, price, amount, TRADE_TYPE)
            trades.append({
                'slack_webhook_url': asset['api']['slack_webhook_url'],
                'exchange': asset['exchange'],
                'symbol': asset['symbol'],
                'side': new_side,
                'price': price
            })
    notify_trades(trades)
    execute_trades(select_unexecuted_trades())
    close_database()

def execute_trades(trades):
    """
    Execute trades
    """
    for trade in trades:
        if trade['exchange'] == 'bitflyer':
            amount = (-1 if trade['side'] == 'sell' else 1) * trade['amount']
            is_executed = bitflyer_trade({
                'key': trade['api']['bitflyer_api_key'],
                'secret': trade['api']['bitflyer_api_secret']
            }, trade['symbol'], trade['type'], amount)
            if is_executed:
                update_trade(trade['id'])
        else:
            update_trade(trade['id'])

if __name__ == "__main__":
    main()
