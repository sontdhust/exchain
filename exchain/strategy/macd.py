"""
MACD
"""

def analyse_macd(
        histograms, situations,
        monotone_uncertainty, fluctuation_uncertainty, difference_dispersity):
    """
    Analyse MACD
    """
    position = 'hold'
    macds = [h['macd'] for h in histograms]
    differences = [h['macd'] - h['signal'] for h in histograms]
    macd_mean = sum(macds) / len(macds)
    macd_range = sum([abs(m - macd_mean) for m in macds]) / len(macds) * 2
    fluctuation = macds[-1] - macd_mean
    difference_mean = sum(differences) / len(differences)
    for situation in situations:
        ticks_count = situation['monotonic_ticks_count']
        last_differences = differences[-ticks_count:]
        monotonicity = check_monotonicity(last_differences, monotone_uncertainty)
        previous_fluctuation = macds[-ticks_count] - macd_mean
        last_difference_mean = sum(last_differences) / len(last_differences)
        if (monotonicity is None
                or monotonicity != (fluctuation > previous_fluctuation)
                or (abs(fluctuation - previous_fluctuation)
                    <= abs(previous_fluctuation) * fluctuation_uncertainty)
                or abs(last_difference_mean) < abs(difference_mean) * (1 - difference_dispersity)):
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

def check_monotonicity(period, monotone_uncertainty):
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
        if abs(value - previous_value) > abs(previous_value) * monotone_uncertainty:
            current_monotonicity = True if value > previous_value else False
            previous_value = value
            if monotonicity is None:
                monotonicity = current_monotonicity
            elif monotonicity != current_monotonicity:
                return None
    return monotonicity
