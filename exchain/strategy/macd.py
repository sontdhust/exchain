"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False
UP = True
DOWN = False

def analyse_macd(histograms, monotonic_period, movement_period, trend_strength_disparity):
    """
    Analyse MACD
    """
    macds = [h['macd'] for h in histograms]
    divergences = [h['macd'] - h['signal'] for h in histograms]
    monotonicity = check_monotonicity(divergences[-monotonic_period:])
    extrema = find_extrema(histograms, movement_period)
    if (monotonicity is None
            or monotonicity != check_monotonicity(macds[-monotonic_period:])
            or len(extrema) < 3):
        return 'hold'
    disparity = find_trend_strength_disparity(extrema) ** (1 if monotonicity is INCREASING else -1)
    if disparity > trend_strength_disparity:
        return 'buy' if monotonicity is INCREASING else 'sell'
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
            'macd': histograms[i]['macd'],
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
            'macd': ext([m['macd'] for m in movement], extremum_type),
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
                        'macd': ext([extremum['macd'], all_extrema[i]['macd']], extremum['type']),
                        'price': ext([extremum['price'], all_extrema[i]['price']], extremum['type'])
                    }
                    continue
                else:
                    essential_extrema.insert(0, extremum)
            extremum = {
                'type': all_extrema[i]['type'],
                'macd': all_extrema[i]['macd'],
                'price': all_extrema[i]['price'],
            }
        essential_extrema.insert(0, extremum)
        return essential_extrema
    return find_essential_extrema([find_extremum(m) for m in movements], movement_period)

def find_trend_strength_disparity(extrema):
    """
    Find trend strength disparity
    """
    def find_trend(first_extremum, second_extremum):
        """
        Find trend
        """
        return {
            'value': UP if (
                first_extremum['type'] is MINIMUM and second_extremum['type'] is MAXIMUM
            ) else (DOWN if (
                first_extremum['type'] is MAXIMUM and second_extremum['type'] is MINIMUM
            ) else None),
            'strength': float(abs(second_extremum['price'] - first_extremum['price']))
        }
    first_strength = find_trend(extrema[-3], extrema[-2])['strength']
    second_trend = find_trend(extrema[-2], extrema[-1])
    return (second_trend['strength'] / first_strength) ** (1 if second_trend['value'] is UP else -1)

def ext(values, extremum_type):
    """
    Ext
    """
    return max(values) if extremum_type is MAXIMUM else min(values)
