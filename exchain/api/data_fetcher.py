"""
Data Fetcher
"""

import urllib2
import time
import json

def fetch_prices(exchange, pair, interval, period):
    """
    Fetch prices
    """
    candles = fetch_candles(exchange, pair, [interval], period)[str(interval)]
    prices = [{'time': c[0], 'close': float(c[4])} for c in candles]
    return prices

def fetch_candles(exchange, pair, intervals, period):
    """
    Fetch candles
    """
    now = int(time.time())
    return json.loads(urllib2.urlopen(
        'https://api.cryptowat.ch/markets/'
        + exchange + '/'
        + pair + '/ohlc'
        + '?periods=' + ','.join([str(i) for i in intervals])
        + '&before=' + str(now)
        + '&after=' + str(now - period * max(intervals))
    ).read())['result']
