"""
Database
"""

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
        'SELECT exchange, pair '
        'FROM users JOIN tickers ON users.id = tickers.user_id '
        'WHERE priority > 0'
    )
    DATABASE['cursor'].execute(query)
    result = [{'exchange': t[0], 'pair': t[1]} for t in DATABASE['cursor'].fetchall()]
    return result

def close_database():
    """
    Close database
    """
    DATABASE['cursor'].close()
    DATABASE['connector'].close()
