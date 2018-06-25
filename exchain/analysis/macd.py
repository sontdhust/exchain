"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False

def analyze_macd(histograms, monotonic_period):
    """
    Analyze MACD
    """
    divergences = [h['macd'] - h['signal'] for h in histograms]
    is_upside = divergences[-1] > 0
    monotonicity = check_monotonicity(divergences[-monotonic_period:])
    macds = [h['macd'] for h in histograms]
    signals = [h['signal'] for h in histograms]
    prices = [h['price'] for h in histograms]
    if (monotonicity is not None
            and monotonicity == check_monotonicity(macds[-monotonic_period:])
            and monotonicity == check_monotonicity(signals[-monotonic_period:])
            and monotonicity == check_monotonicity(prices[-monotonic_period:])
            and (monotonicity is INCREASING) == is_upside):
        return 'buy' if is_upside else 'sell'
    return 'hold'

def check_monotonicity(period):
    """
    Check monotonicity
    """
    monotonicity = None
    previous_value = None
    if len(period) < 2:
        return monotonicity
    for i in range(0, len(period)):
        value = period[i]
        if i == 0:
            previous_value = value
            continue
        current_monotonicity = INCREASING if value > previous_value else DECREASING
        previous_value = value
        if monotonicity is None:
            monotonicity = current_monotonicity
        elif monotonicity != current_monotonicity:
            return None
    return monotonicity
