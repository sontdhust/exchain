"""
MACD
"""

def analyse_macd(histograms, situations, monotonicity_variation, difference_dispersion):
    """
    Analyse MACD
    """
    macds = [h['macd'] for h in histograms]
    differences = [h['macd'] - h['signal'] for h in histograms]
    macd_mean = sum(macds) / len(macds)
    macd_range = sum([abs(m - macd_mean) for m in macds]) / len(macds) * 2
    fluctuation = macds[-1] - macd_mean
    difference_mean = sum(differences) / len(differences)
    position = 'hold'
    for situation in situations:
        ticks_count = situation['monotonic_ticks_count']
        last_differences = differences[-ticks_count:]
        monotonicity = check_monotonicity(last_differences, monotonicity_variation)
        last_difference_mean = sum(last_differences) / len(last_differences)
        if (monotonicity is None
                or monotonicity != (macds[-1] > macds[-ticks_count])
                or abs(last_difference_mean) < abs(difference_mean) * (1 - difference_dispersion)):
            continue
        relative_fluctuation = fluctuation * (-1 if monotonicity else 1)
        fluctuation_bound = situation['fluctuation_bound']
        if fluctuation_bound is not None:
            is_reversing = (
                '<' in fluctuation_bound
                and relative_fluctuation < macd_range * float(fluctuation_bound.replace('<', ''))
            )
            is_reversing = is_reversing or (
                '~' in fluctuation_bound
                and relative_fluctuation > macd_range * float(fluctuation_bound.split('~')[0])
                and relative_fluctuation < macd_range * float(fluctuation_bound.split('~')[1])
            )
            is_reversing = is_reversing or (
                '>' in fluctuation_bound
                and relative_fluctuation > macd_range * float(fluctuation_bound.replace('>', ''))
            )
            if is_reversing:
                position = 'buy' if monotonicity else 'sell'
                break
        else:
            position = 'buy' if monotonicity else 'sell'
            break
    return position

def check_monotonicity(period, monotonicity_variation):
    """
    Check monotonicity
    """
    monotonicity = None
    last_value = None
    if len(period) < 2:
        return monotonicity
    for i in range(0, len(period)):
        value = period[i]
        if i == 0:
            last_value = value
            continue
        if abs(value - last_value) > abs(last_value) * monotonicity_variation:
            current_monotonicity = True if value > last_value else False
            last_value = value
            if monotonicity is None:
                monotonicity = current_monotonicity
            elif monotonicity != current_monotonicity:
                return None
    return monotonicity
