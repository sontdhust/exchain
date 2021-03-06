"""
Exchange
"""

import time
import json
import urllib
import hmac
import hashlib
import requests

BUY = 'BUY'
SELL = 'SELL'
FRACTION = 2

def bitflyer_trade(api, symbol, overall_type, amount):
    """
    Bitflyer trade
    """
    order_type = overall_type.upper()
    positions = bitflyer_get_positions(api, symbol)
    if positions is None:
        return False
    buy_size = sum([p['size'] for p in positions if p['side'] == BUY])
    sell_size = sum([p['size'] for p in positions if p['side'] == SELL])
    size = round(amount - (buy_size - sell_size), FRACTION)
    if size == 0:
        return True
    bitflyer_send_child_order(api, symbol, order_type, BUY if size > 0 else SELL, abs(size))
    return False

def bitflyer_get_positions(api, product_code):
    """
    Bitflyer get positions
    """
    return bitflyer_request(api, 'GET', '/v1/me/getpositions', {
        'product_code': product_code
    })

def bitflyer_send_child_order(api, product_code, order_type, side, size):
    """
    Bitflyer send child order
    """
    return bitflyer_request(api, 'POST', '/v1/me/sendchildorder', {
        'product_code': product_code,
        'child_order_type': order_type,
        'side': side,
        'size': size
    })

def bitflyer_request(api, method, endpoint, parameters):
    """
    Bitflyer request
    """
    if api['key'] is None or api['key'] == '' or api['secret'] is None or api['secret'] == '':
        return None
    timestamp = str(time.time())
    body = ''
    if method == 'POST':
        body = json.dumps(parameters)
    else:
        body = '?' + urllib.urlencode(parameters)
    text = timestamp + method + endpoint + body
    sign = hmac.new(api['secret'].encode(), text.encode(), hashlib.sha256).hexdigest()
    header = {
        'ACCESS-KEY': api['key'],
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-SIGN': sign,
        'Content-Type': 'application/json'
    }
    url = 'https://api.bitflyer.jp' + endpoint
    try:
        with requests.Session() as session:
            session.headers.update(header)
            if method == 'GET':
                response = session.get(url, params=parameters)
            else:
                response = session.post(url, data=json.dumps(parameters))
    except requests.RequestException as exception:
        raise exception
    content = ''
    if len(response.content) > 0:
        content = json.loads(response.content.decode('utf-8'))
    return content
