"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False
UP = True
DOWN = False

def analyse_macd(histograms, monotonic_period, movement_period, situations):
    """
    Analyse MACD
    """
    macds = [h['macd'] for h in histograms]
    monotonicity = check_monotonicity(
        [h['macd'] - h['signal'] for h in histograms][-monotonic_period:]
    )
    extrema = find_extrema(histograms, movement_period)
    if (monotonicity is None
            or monotonicity != check_monotonicity(macds[-monotonic_period:])
            or len(extrema) < 3):
        return 'hold'
    previous_extremum = [e for e in extrema[:-1] if (
        (monotonicity is INCREASING and e['type'] is MAXIMUM)
        or (monotonicity is DECREASING and e['type'] is MINIMUM)
    )][-1]
    dispersity = (
        (macds[-1] - previous_extremum['macd'])
        * (-1 if monotonicity is INCREASING else 1)
        / find_standard_deviation(macds)
    )
    disparity = find_trend_strength_disparity(extrema) ** (1 if monotonicity is INCREASING else -1)
    def is_inside_domain(number, domain):
        """
        Is inside domain
        """
        if domain is None:
            return True
        is_inside = (
            '<' in domain
            and number < float(domain.replace('<', ''))
        )
        is_inside = is_inside or (
            '~' in domain
            and number > float(domain.split('~')[0])
            and number < float(domain.split('~')[1])
        )
        is_inside = is_inside or (
            '>' in domain
            and number > float(domain.replace('>', ''))
        )
        return is_inside
    for situation in situations:
        if (is_inside_domain(dispersity, situation['macd_dispersity_domain'])
                and is_inside_domain(disparity, situation['trend_strength_disparity_domain'])):
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
            else:
                if len(extremum) != 0:
                    if extremum['type'] == all_extrema[i]['type']:
                        extremum = {
                            'type': extremum['type'],
                            'macd': ext(
                                [extremum['macd'], all_extrema[i]['macd']],
                                extremum['type']
                            ),
                            'price': ext(
                                [extremum['price'], all_extrema[i]['price']],
                                extremum['type']
                            )
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

def find_standard_deviation(values):
    """
    Find standard deviation
    """
    mean = sum(values) / len(values)
    variance = sum([(v - mean) ** 2 for v in values]) / len(values)
    standard_deviation = variance ** 0.5
    return standard_deviation

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
            'strength': abs(second_extremum['price'] - first_extremum['price'])
        }
    first_trend = find_trend(extrema[-3], extrema[-2])
    second_trend = find_trend(extrema[-2], extrema[-1])
    return (
        (second_trend['strength'] / first_trend['strength'])
        ** (1 if second_trend['value'] is UP else -1)
    )

def ext(values, extremum_type):
    """
    Ext
    """
    return max(values) if extremum_type is MAXIMUM else min(values)
