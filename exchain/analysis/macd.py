"""
MACD
"""

INCREASING = True
DECREASING = False

def analyze_macd(histograms, monotonic_period):
    """
    Analyze MACD
    """
    macds = [h['macd'] for h in histograms]
    signals = [h['signal'] for h in histograms]
    divergences = [h['macd'] - h['signal'] for h in histograms]
    is_crossover = divergences[-1] * divergences[-2] < 0 or divergences[-1] * divergences[-3] < 0
    is_upside = divergences[-1] > 0
    monotonicity = check_monotonicity(macds[-monotonic_period:])
    if (monotonicity is not None
            and check_monotonicity(signals[-monotonic_period:]) == monotonicity
            and is_crossover
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
