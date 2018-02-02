"""
MACD
"""

FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9

def calculate_macd_histograms(prices):
    """
    Calulate MACD histograms
    """
    fast_multiplier = 2.0 / (FAST_PERIOD + 1)
    slow_multiplier = 2.0 / (SLOW_PERIOD + 1)
    signal_multiplier = 2.0 / (SIGNAL_PERIOD + 1)
    fast = calculate_sma(prices, FAST_PERIOD - 1, SLOW_PERIOD - 1)
    slow = calculate_sma(prices, 0, SLOW_PERIOD - 1)
    macds = []
    for price in prices[SLOW_PERIOD:]:
        fast += (price['value'] - fast) * fast_multiplier
        slow += (price['value'] - slow) * slow_multiplier
        macds.append({'time': price['time'], 'value': fast - slow})
    signal = calculate_sma(macds, 0, SIGNAL_PERIOD - 1)
    macd_histograms = []
    for macd in macds[SIGNAL_PERIOD:]:
        signal += (macd['value'] - signal) * signal_multiplier
        macd_histograms.append({'time': macd['time'], 'macd': macd['value'], 'signal': signal})
    return macd_histograms

def calculate_sma(prices, start, end):
    """
    Calculate SMA
    """
    sma = 0
    for i in range(start, end):
        sma += float(prices[i]['value'])
    return sma
