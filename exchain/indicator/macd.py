"""
MACD
"""

FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9

def calculate_macd_histograms(prices):
    """
    Calculate MACD histograms
    """
    fast_multiplier = 2.0 / (FAST_PERIOD + 1)
    slow_multiplier = 2.0 / (SLOW_PERIOD + 1)
    signal_multiplier = 2.0 / (SIGNAL_PERIOD + 1)
    fast = calculate_sma(prices, 'close', FAST_PERIOD - 1, SLOW_PERIOD - 1)
    slow = calculate_sma(prices, 'close', 0, SLOW_PERIOD - 1)
    macds = []
    for price in prices[SLOW_PERIOD:]:
        fast += (price['close'] - fast) * fast_multiplier
        slow += (price['close'] - slow) * slow_multiplier
        macds.append({'time': price['time'], 'value': fast - slow, 'price': price['close']})
    signal = calculate_sma(macds, 'value', 0, SIGNAL_PERIOD - 1)
    macd_histograms = []
    for macd in macds[SIGNAL_PERIOD:]:
        signal += (macd['value'] - signal) * signal_multiplier
        macd_histograms.append({
            'time': macd['time'],
            'macd': macd['value'],
            'signal': signal,
            'price': macd['price']
        })
    return macd_histograms

def calculate_sma(period, key, start, end):
    """
    Calculate SMA
    """
    sma = 0
    for i in range(start, end + 1):
        sma += period[i][key]
    return sma
