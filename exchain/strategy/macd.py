"""
MACD
"""

INCREASING = True
DECREASING = False
MAXIMUM = True
MINIMUM = False
UP = True
DOWN = False
BULL = True
BEAR = False

def analyse_macd(histograms, movement_period, trend_strength_disparity):
    """
    Analyse MACD
    """
    extrema = find_extrema(histograms)
    sentiment = find_sentiment(extrema, movement_period, trend_strength_disparity)
    return 'hold' if sentiment is None else ('buy' if sentiment is BULL else 'sell')

def find_extrema(histograms):
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
            'macd': ext([r['macd'] for r in movement], extremum_type),
            'price': ext([r['price'] for r in movement], extremum_type),
        }
    return [find_extremum(m) for m in movements]

def find_sentiment(extrema, movement_period, trend_strength_disparity):
    """
    Find sentiment
    """
    essential_extrema = []
    extremum = {}
    for i in range(len(extrema) - 1, -1, -1):
        if extrema[i]['period'] < movement_period:
            continue
        else:
            if len(extremum) != 0:
                if extremum['type'] == extrema[i]['type']:
                    extremum = {
                        'type': extremum['type'],
                        'macd': ext([extremum['macd'], extrema[i]['macd']], extremum['type']),
                        'price': ext([extremum['price'], extrema[i]['price']], extremum['type'])
                    }
                    continue
                else:
                    essential_extrema.insert(0, extremum)
            extremum = {
                'type': extrema[i]['type'],
                'macd': extrema[i]['macd'],
                'price': extrema[i]['price'],
            }
    essential_extrema.insert(0, extremum)
    if len(essential_extrema) < 3:
        return None
    def find_trend(first_extremum, second_extremum):
        """
        Find trend
        """
        return {
            'trend': UP if (
                first_extremum['type'] is MINIMUM and second_extremum['type'] is MAXIMUM
            ) else (DOWN if (
                first_extremum['type'] is MAXIMUM and second_extremum['type'] is MINIMUM
            ) else None),
            'strength': (
                abs(first_extremum['price'] - second_extremum['price'])
                / abs(first_extremum['macd'] - second_extremum['macd'])
            )
        }
    first_trend = find_trend(essential_extrema[-3], essential_extrema[-2])
    second_trend = find_trend(essential_extrema[-2], essential_extrema[-1])
    if first_trend['strength'] < (1 - trend_strength_disparity) * second_trend['strength']:
        return BULL if second_trend['trend'] is UP else BEAR
    if second_trend['strength'] < (1 - trend_strength_disparity) * first_trend['strength']:
        return BULL if first_trend['trend'] is UP else BEAR

def ext(series, extremum_type):
    """
    Ext
    """
    return max(series) if extremum_type is MAXIMUM else min(series)
