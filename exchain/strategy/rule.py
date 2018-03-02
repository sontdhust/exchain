"""
Rule
"""

from collections import Counter

def identify_side(sides, consensus_threshold):
    """
    Identify side
    """
    most_common = Counter(sides).most_common(2)
    if (len(most_common) == 1
            or len(most_common) > 1
            and most_common[0][1] > most_common[1][1]
            and most_common[0][1] >= int(len(sides) * consensus_threshold)):
        return most_common[0][0]
    else:
        return None
