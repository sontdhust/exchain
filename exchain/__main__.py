"""
Exchain
"""

from config import read_config
from api import fetch_prices
from indicator import calculate_macd_histograms

def main():
    """
    Main function
    """
    prices = fetch_prices(
        exchange='bitfinex',
        pair='btcusd',
        interval=read_config('api.interval'),
        ticks_count=read_config('api.ticks_count')
    )
    macd_histograms = calculate_macd_histograms(prices)
    print macd_histograms

if __name__ == "__main__":
    main()
