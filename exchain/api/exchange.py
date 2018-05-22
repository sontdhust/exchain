"""
Exchange
"""

import time
import json
import urllib
import hmac
import hashlib
import requests

def bitflyer_get_positions(api, product_code):
    """
    Bitflyer get positions
    """
    return bitflyer_request(api['key'], api['secret'], 'GET', '/v1/me/getpositions', {
        'product_code': product_code
    })

def bitflyer_send_child_order(api, product_code, order_type, side, size):
    """
    Bitflyer send child order
    """
    return bitflyer_request(api['key'], api['secret'], 'POST', '/v1/me/sendchildorder', {
        'product_code': product_code,
        'child_order_type': order_type,
        'side': side,
        'size': size
    })

def bitflyer_request(api_key, api_secret, method, endpoint, parameters):
    """
    Bitflyer request
    """
    if api_key is None or api_key == '' or api_secret is None or api_secret == '':
        return
    timestamp = str(time.time())
    body = ''
    if method == 'POST':
        body = json.dumps(parameters)
    else:
        body = '?' + urllib.urlencode(parameters)
    text = timestamp + method + endpoint + body
    sign = hmac.new(api_secret.encode(), text.encode(), hashlib.sha256).hexdigest()
    header = {
        'ACCESS-KEY': api_key,
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
