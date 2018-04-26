"""
Database
"""

import datetime
import json
import mysql.connector

DATABASE = {'connector': None, 'cursor': None}

def connect_database(config):
    """
    Connect database
    """
    DATABASE['connector'] = mysql.connector.connect(**config)
    DATABASE['cursor'] = DATABASE['connector'].cursor()

def close_database():
    """
    Close database
    """
    DATABASE['cursor'].close()
    DATABASE['connector'].close()

def select_tickers():
    """
    Select tickers
    """
    query = (
        'SELECT id, exchange, pair, priority '
        'FROM tickers '
        'ORDER BY id'
    )
    DATABASE['cursor'].execute(query)
    result = [{
        'id': r[0],
        'exchange': r[1],
        'pair': r[2],
        'priority': r[3]
    } for r in DATABASE['cursor'].fetchall()]
    return result

def update_ticker(ticker_id, side, price):
    """
    Update ticker
    """
    query = (
        'UPDATE tickers '
        'SET side = %(side)s, price = %(price)s, updated_at = %(updated_at)s '
        'WHERE id = %(id)s'
    )
    DATABASE['cursor'].execute(query, {
        'id': ticker_id,
        'side': side,
        'price': price,
        'updated_at': get_current_datetime()
    })
    DATABASE['connector'].commit()

def select_assets():
    """
    Select assets
    """
    query = (
        'SELECT assets.id, tickers.id, api, exchange, pair, amount '
        'FROM assets '
        'JOIN users ON assets.user_id = users.id '
        'JOIN tickers ON assets.ticker_id = tickers.id '
        'WHERE assets.priority > 0 '
        'ORDER BY assets.id'
    )
    DATABASE['cursor'].execute(query)
    def load_api(text):
        """
        Load api
        """
        default_api = {
            'slack_webhook_url': ''
        }
        api = json.loads(text) if text is not None else {}
        api.update({k: v for k, v in default_api.iteritems() if k not in api})
        return api
    result = [{
        'id': r[0],
        'ticker_id': r[1],
        'api': load_api(r[2]),
        'exchange': r[3],
        'pair': r[4],
        'amount': r[5]
    } for r in DATABASE['cursor'].fetchall()]
    return result

def select_previous_trade(asset_id):
    """
    Select previous trade
    """
    query = (
        'SELECT side '
        'FROM trades '
        'WHERE asset_id = %(asset_id)s '
        'ORDER BY id DESC '
        'LIMIT 1'
    )
    DATABASE['cursor'].execute(query, {'asset_id': asset_id})
    result = [{'side': r[0]} for r in DATABASE['cursor'].fetchall()]
    if len(result) == 0:
        return None
    else:
        return result[0]

def insert_trade(asset_id, side, price, amount, trade_type):
    """
    Insert trade
    """
    query = (
        'INSERT INTO trades (asset_id, side, price, amount, type, created_at) '
        'VALUES (%(asset_id)s, %(side)s, %(price)s, %(amount)s, %(type)s, %(created_at)s)'
    )
    DATABASE['cursor'].execute(query, {
        'asset_id': asset_id,
        'side': side,
        'price': price,
        'amount': amount,
        'type': trade_type,
        'created_at': get_current_datetime()
    })
    DATABASE['connector'].commit()

def get_current_datetime():
    """
    Get current datetime
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
