"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False

def analyse_macd(histograms, monotonic_period, movement_period):
    """
    Analyse MACD
    """
    macds = [h['macd'] for h in histograms]
    divergences = [h['macd'] - h['signal'] for h in histograms]
    monotonicity = check_monotonicity(divergences[-monotonic_period:])
    extrema = find_extrema(histograms, movement_period)
    if (monotonicity is None
            or monotonicity != check_monotonicity(macds[-monotonic_period:])):
        return 'hold'
    is_increasing = monotonicity is INCREASING
    if (is_increasing == (extrema[-1]['type'] is MAXIMUM)
            and is_increasing == (histograms[-1]['price'] > extrema[-1]['price'])
            or divergences[-1] * divergences[-2] < 0):
        return 'buy' if is_increasing else 'sell'
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
            'price': ext([m['price'] for m in movement], extremum_type),
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
                    extremum = {
                        'type': extremum['type'],
                        'price': ext([extremum['price'], all_extrema[i]['price']], extremum['type'])
                    }
                    continue
                else:
                    essential_extrema.insert(0, extremum)
            extremum = {
                'type': all_extrema[i]['type'],
                'price': all_extrema[i]['price'],
            }
        essential_extrema.insert(0, extremum)
        return essential_extrema
    return find_essential_extrema([find_extremum(m) for m in movements], movement_period)

def ext(values, extremum_type):
    """
    Ext
    """
    return max(values) if extremum_type is MAXIMUM else min(values)
