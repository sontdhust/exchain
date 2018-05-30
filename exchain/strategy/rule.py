"""
Rule
"""

from collections import Counter

def identify_overall_side(sides, consensus_threshold):
    """
    Identify overall side
    """
    most_common = Counter(sides).most_common(2)
    if (len(most_common) == 1
            or len(most_common) > 1
            and most_common[0][1] > most_common[1][1]
            and most_common[0][1] >= int(len(sides) * consensus_threshold)):
        return most_common[0][0]
    else:
        return None

def check_reversal(previous_trade, side):
    """
    Check reversal
    """
    if side == 'hold':
        return False
    if previous_trade is None:
        return True
    previous_position = previous_trade['side'].split('-')[0]
    position = side.split('-')[0]
    return previous_position != position
