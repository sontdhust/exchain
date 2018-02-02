"""
MACD
"""

MAXIMUM = True

def analyse_macd(histograms, difference_monotonic_period, difference_period, macd_dispersity):
    """
    Analyse MACD
    """
    macds = [h['macd'] for h in histograms]
    macd_mean = sum(macds) / len(macds)
    macd_variance = sum([(m - macd_mean) ** 2 for m in macds]) / len(macds)
    macd_standard_deviation = macd_variance ** 0.5
    differences = [h['macd'] - h['signal'] for h in histograms]
    monotonicity = check_monotonicity(differences[-difference_monotonic_period:])
    if monotonicity is None or monotonicity != (macds[-1] > macds[-difference_monotonic_period]):
        return 'hold'
    else:
        extremum = find_previous_extremum(
            macds, differences, monotonicity is True, difference_period
        )
        if extremum is None:
            return 'hold'
        else:
            if ((macds[-1] - extremum) * (-1 if monotonicity else 1)
                    > macd_standard_deviation * macd_dispersity):
                return 'buy' if monotonicity else 'sell'
            else:
                return 'hold'

def find_previous_extremum(macds, differences, extremum_type, difference_period):
    """
    Find previous extremum
    """
    extremum = None
    is_started_finding = False
    count = 0
    for i in range(len(differences) - 1, -1, -1):
        if not (extremum_type is MAXIMUM) ^ (differences[i] < 0):
            if extremum is None:
                is_started_finding = True
                continue
            else:
                if count < difference_period:
                    extremum = None
                    count = 0
                else:
                    break
        else:
            if not is_started_finding:
                continue
            macd = macds[i]
            count += 1
            if extremum is None:
                extremum = macd
            else:
                extremum = max(extremum, macd) if extremum_type is MAXIMUM else min(extremum, macd)
    return extremum

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
