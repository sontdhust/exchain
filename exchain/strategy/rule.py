"""
Rule
"""

from collections import Counter

def consider_side(sides, side, consensus_threshold):
    """
    Consider side
    """
    most_common = Counter(sides).most_common(2)
    if (len(most_common) == 1
            or len(most_common) > 1
            and most_common[0][1] > most_common[1][1]
            and most_common[0][1] >= int(len(sides) * consensus_threshold)):
        overall_side = most_common[0][0]
        if side == 'hold' or side == overall_side:
            return overall_side
        else:
            return side if overall_side == 'hold' else 'hold'
    else:
        if side == 'buy' or side == 'sell':
            count = len([s for s in sides if s == side or s == 'hold'])
            return side if count >= int(len(sides) * consensus_threshold) else None
        else:
            return None

def check_reversal(previous_trade, side):
    """
    Check reversal
    """
    if previous_trade is None:
        return True
    previous_side = previous_trade['side']
    return previous_side != side
