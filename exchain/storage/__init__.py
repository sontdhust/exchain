"""
Storage
"""

from storage.config import read_config
from storage.database import (
    connect_database, close_database,
    select_tickers, update_ticker,
    select_assets,
    select_previous_trade, insert_trade, select_unexecuted_trades, update_trade
)
