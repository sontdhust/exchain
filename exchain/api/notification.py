"""
Notification
"""

import json
import math
import decimal
import requests

def notify_trades(url, trades, side):
    """
    Notify trades
    """
    text = '\n'.join([(
        '*' + t['pair'].upper()
        + '* (_' + t['exchange'].title() + '_): '
        + format_price(t['price']) + '.'
    ) for t in trades])
    send_slack_message(url, '', [{
        'fallback': side.title() + '.',
        'text': text,
        'color': 'good' if 'buy' in side else 'danger',
        'mrkdwn_in': ['text']
    }])

def send_slack_message(webhook_url, text, attachments):
    """
    Send Slack message
    """
    if webhook_url is None or webhook_url == '':
        return
    requests.post(webhook_url, json.dumps({
        'text': text,
        'mrkdwn': True,
        'attachments': attachments
    }), {
        'Content-Type': 'application/json'
    })

def format_price(price, max_fractional=5):
    """
    Format price
    """
    integer = 1
    if price != 0:
        logarithm = math.log10(price)
        integer = int(logarithm) + (1 if logarithm > 0 else 0)
    fractional = max_fractional - integer if integer < max_fractional else 0
    return str(decimal.Decimal(('{:.' + str(fractional) + 'f}').format(price)).normalize())
