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
    divergences = [h['macd'] - h['signal'] for h in histograms]
    is_upside = divergences[-1] > 0
    levels = [e for e in find_levels(histograms, movement_period) if (
        e['type'] == (MINIMUM if is_upside else MAXIMUM)
    )]
    if len(levels) > 0 and is_upside == (histograms[-1]['price'] < levels[-1]['last_price']):
        return ('sell' if is_upside else 'buy') + '-close'
    monotonicity = check_monotonicity(divergences[-monotonic_period:])
    macds = [h['macd'] for h in histograms]
    signals = [h['signal'] for h in histograms]
    prices = [h['price'] for h in histograms]
    if (monotonicity is not None
            and monotonicity == check_monotonicity(macds[-monotonic_period:])
            and monotonicity == check_monotonicity(signals[-monotonic_period:])
            and monotonicity == check_monotonicity(prices[-monotonic_period:])
            and (monotonicity is INCREASING) == is_upside):
        return ('buy' if is_upside else 'sell') + '-open'
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

def find_levels(histograms, movement_period):
    """
    Find levels
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
    def find_level(movement):
        """
        Find level
        """
        level_type = MAXIMUM if movement[-1]['divergence'] > 0 else MINIMUM
        return {
            'type': level_type,
            'period': len(movement),
            'last_price': movement[-1]['price'],
        }
    def find_essential_levels(all_levels, movement_period):
        """
        Find essential levels
        """
        essential_levels = []
        level = {}
        for i in range(len(all_levels) - 1, -1, -1):
            if all_levels[i]['period'] < movement_period:
                continue
            if len(level) != 0:
                if level['type'] == all_levels[i]['type']:
                    continue
                else:
                    essential_levels.insert(0, level)
            level = {
                'type': all_levels[i]['type'],
                'last_price': all_levels[i]['last_price'],
            }
        essential_levels.insert(0, level)
        return essential_levels
    return find_essential_levels([find_level(m) for m in movements], movement_period)
