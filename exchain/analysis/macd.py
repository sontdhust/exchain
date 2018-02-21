"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False

def analyze_macd(histograms, monotonic_period, movement_period):
    """
    Analyze MACD
    """
    macds = [h['macd'] for h in histograms]
    divergences = [h['macd'] - h['signal'] for h in histograms]
    is_upside = divergences[-1] > 0
    last_extremum = [e for e in find_extrema(histograms, movement_period) if (
        e['type'] == (MINIMUM if is_upside else MAXIMUM)
    )][-1]
    if is_upside == (histograms[-1]['price'] < last_extremum['last_price']):
        return 'sell' if is_upside else 'buy'
    monotonicity = check_monotonicity(divergences[-monotonic_period:])
    if (monotonicity is not None
            and monotonicity == check_monotonicity(macds[-monotonic_period:])
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

def find_extrema(histograms, movement_period):
    """
    Find extrema
    """
    movements = []
    movement = []
    for i in range(len(histograms) - 1, -1, -1):
        divergence = histograms[i]['macd'] - histograms[i]['signal']
        if len(movement) != 0 and divergence * movement[-1]['divergence'] < 0:
            movements.insert(0, movement)
            movement = []
        movement.insert(0, {
            'divergence': divergence,
            'price': histograms[i]['price']
        })
    def find_extremum(movement):
        """
        Find extremum
        """
        extremum_type = MAXIMUM if movement[-1]['divergence'] > 0 else MINIMUM
        return {
            'type': extremum_type,
            'period': len(movement),
            'last_price': movement[-1]['price'],
        }
    def find_essential_extrema(all_extrema, movement_period):
        """
        Find essential extrema
        """
        essential_extrema = []
        extremum = {}
        for i in range(len(all_extrema) - 1, -1, -1):
            if all_extrema[i]['period'] < movement_period:
                continue
            if len(extremum) != 0:
                if extremum['type'] == all_extrema[i]['type']:
                    continue
                else:
                    essential_extrema.insert(0, extremum)
            extremum = {
                'type': all_extrema[i]['type'],
                'last_price': all_extrema[i]['last_price'],
            }
        essential_extrema.insert(0, extremum)
        return essential_extrema
    return find_essential_extrema([find_extremum(m) for m in movements], movement_period)
