"""
RSI
"""

PERIOD = 14

def calculate_rsi(prices):
    """
    Calculate RSI
    """
    gain = 0.0
    loss = 0.0
    for i in range(0, len(prices)):
        if i == 0:
            continue
        change = prices[i]['value'] - prices[i - 1]['value']
        current_gain = change if change > 0 else 0
        current_loss = -change if change < 0 else 0
        if i <= PERIOD:
            gain += current_gain
            loss += current_loss
            if i == PERIOD:
                gain = gain / PERIOD
                loss = loss / PERIOD
        else:
            gain = (gain * (PERIOD - 1) + current_gain) / PERIOD
            loss = (loss * (PERIOD - 1) + current_loss) / PERIOD
    rsi = 100 - 100 / (1 + gain / loss)
    return {'time': prices[-1]['time'], 'rsi': rsi, 'price': prices[-1]['value']}
