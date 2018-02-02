"""
RSI
"""

def analyze_rsi(rsi, oversold_level, overbought_level):
    """
    Analyze RSI
    """
    rsi = rsi['rsi']
    if rsi < oversold_level:
        return 'buy'
    elif rsi > overbought_level:
        return 'sell'
    else:
        return 'hold'
