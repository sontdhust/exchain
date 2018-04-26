"""
Data Fetcher
"""

import urllib2
import time
import json

def fetch_points(exchange, pair, interval, period):
    """
    Fetch points
    """
    candles = fetch_candles(exchange, pair, [interval], period)[str(interval)]
    prices = [{'time': c[0], 'close': float(c[4])} for c in candles]
    previous_candle = candles[-2]
    previous_pivot = (previous_candle[2] + previous_candle[3] + previous_candle[4]) / 3.0
    return (prices, previous_pivot)

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
