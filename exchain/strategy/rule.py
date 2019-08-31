"""
Rule
"""

from collections import Counter
from datetime import datetime

def decide_side(sides, side, previous_side, consensus_threshold):
    """
    Decide side
    """
    threshold = int(len(sides) * consensus_threshold)
    most_common = Counter(sides).most_common(2)
    if (most_common[0][1] >= threshold
            and (side == 'close' or side == most_common[0][0])):
        return most_common[0][0]
    else:
        return 'close' if check_reversal(previous_side, side) else 'hold'

def check_side_change(previous_trade, side):
    """
    Check side change
    """
    if previous_trade is None:
        return True
    previous_side = previous_trade['side']
    return previous_side != side

def need_to_delay(previous_trade, time):
    """
    Need to delay
    """
    if previous_trade is None or previous_trade['side'] != 'close':
        return False
    elapsed_time = (datetime.now() - previous_trade['created_at']).total_seconds()
    return elapsed_time < time

def check_reversal(previous_side, side):
    """
    Check reversal
    """
    return (previous_side != None and previous_side != 'close'
            and side != 'close' and side != 'hold' and previous_side != side)
