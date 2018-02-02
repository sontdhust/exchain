"""
Data Fetcher
"""

import urllib2
import time
import json

def fetch_prices(exchange, pair, interval, ticks_count):
    """
    Fetch prices
    """
    candles = fetch_candles(exchange, pair, [interval], ticks_count)
    return [{'time': c[0], 'value': c[4]} for c in candles[str(interval)]]

def fetch_candles(exchange, pair, intervals, ticks_count):
    """
    Fetch Candles
    """
    now = int(time.time())
    return json.loads(urllib2.urlopen(
        'https://api.cryptowat.ch/markets/'
        + exchange + '/'
        + pair + '/ohlc'
        + '?periods=' + ','.join([str(i) for i in intervals])
        + '&before=' + str(now)
        + '&after=' + str(now - ticks_count * max(intervals))
    ).read())['result']
