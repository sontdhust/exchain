"""
MACD
"""

def analyse_macd(histograms, situations):
    """
    Analyse MACD
    """
    position = 'hold'
    macds = [h['macd'] for h in histograms]
    differences = [h['macd'] - h['signal'] for h in histograms]
    macd_mean = sum(macds) / len(macds)
    macd_range = sum([abs(m - macd_mean) for m in macds]) / len(macds) * 2
    fluctuation = macds[-1] - macd_mean
    for situation in situations:
        period = situation['monotonic_period']
        last_differences = differences[-period:]
        monotonicity = check_monotonicity(last_differences)
        if monotonicity is None:
            continue
        relative_fluctuation = fluctuation * (-1 if monotonicity else 1)
        fluctuation_domain = situation['fluctuation_domain']
        if fluctuation_domain is not None:
            is_reversing = (
                '<' in fluctuation_domain
                and relative_fluctuation < macd_range * float(fluctuation_domain.replace('<', ''))
            )
            is_reversing = is_reversing or (
                '~' in fluctuation_domain
                and relative_fluctuation > macd_range * float(fluctuation_domain.split('~')[0])
                and relative_fluctuation < macd_range * float(fluctuation_domain.split('~')[1])
            )
            is_reversing = is_reversing or (
                '>' in fluctuation_domain
                and relative_fluctuation > macd_range * float(fluctuation_domain.replace('>', ''))
            )
            if is_reversing:
                position = 'buy' if monotonicity else 'sell'
                break
        else:
            position = 'buy' if monotonicity else 'sell'
            break
    return position

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
        current_monotonicity = True if value > previous_value else False
        previous_value = value
        if monotonicity is None:
            monotonicity = current_monotonicity
        elif monotonicity != current_monotonicity:
            return None
    return monotonicity
