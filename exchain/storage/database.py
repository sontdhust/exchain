"""
Database
"""

import datetime
import mysql.connector

DATABASE = {'connector': None, 'cursor': None}

def connect_database(config):
    """
    Connect database
    """
    DATABASE['connector'] = mysql.connector.connect(**config)
    DATABASE['cursor'] = DATABASE['connector'].cursor()

def select_tickers():
    """
    Select tickers
    """
    query = (
        'SELECT tickers.id, exchange, pair '
        'FROM users JOIN tickers ON users.id = tickers.user_id '
        'WHERE priority > 0'
    )
    DATABASE['cursor'].execute(query)
    result = [{'id': t[0], 'exchange': t[1], 'pair': t[2]} for t in DATABASE['cursor'].fetchall()]
    return result

def select_previous_trade(ticker_id):
    """
    Select previous trade
    """
    query = (
        'SELECT side '
        'FROM trades '
        'WHERE ticker_id = %(ticker_id)s '
        'ORDER BY id DESC '
        'LIMIT 1'
    )
    DATABASE['cursor'].execute(query, {'ticker_id': ticker_id})
    result = [{'side': t[0]} for t in DATABASE['cursor'].fetchall()]
    if len(result) == 0:
        return None
    else:
        return result[0]

def insert_trade(ticker_id, side, price, amount, trade_type):
    """
    Insert trade
    """
    query = (
        'INSERT INTO trades (ticker_id, side, price, amount, type, created_at) '
        'VALUES (%(ticker_id)s, %(side)s, %(price)s, %(amount)s, %(type)s, %(created_at)s)'
    )
    value = {
        'ticker_id': ticker_id,
        'side': side,
        'price': price,
        'amount': amount,
        'type': trade_type,
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    DATABASE['cursor'].execute(query, value)
    DATABASE['connector'].commit()

def close_database():
    """
    Close database
    """
    DATABASE['cursor'].close()
    DATABASE['connector'].close()
