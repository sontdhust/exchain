"""
Notification
"""

import json
import math
import decimal
import requests

def notify_trades(all_trades):
    """
    Notify trades
    """
    for url, grouped_trades in group_elements(all_trades, 'slack_webhook_url'):
        for side, trades in group_elements(grouped_trades, 'side'):
            text = '\n'.join([(
                '*' + t['symbol']
                + '* (_' + t['exchange'].title() + '_): '
                + format_price(t['price']) + '.'
            ) for t in trades])
            send_slack_message(url, '', [{
                'fallback': side.title() + '.',
                'text': text,
                'color': 'warning' if 'hold' in side else ('good' if 'buy' in side else 'danger'),
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

def group_elements(array, key):
    """
    Group elements
    """
    return [(main_key, [{other_key: e[other_key] for other_key in (
        set(e.keys()) - set([key])
    )} for e in array if e[key] == main_key]) for main_key in set(
        [e[key] for e in array]
    )]

def format_price(price, max_fraction=5):
    """
    Format price
    """
    integer = 1
    if price != 0:
        logarithm = math.log10(price)
        integer = int(logarithm) + (1 if logarithm > 0 else 0)
    fraction = max_fraction - integer if integer < max_fraction else 0
    normalized = decimal.Decimal(('{:.' + str(fraction) + 'f}').format(price)).normalize()
    exponent = normalized.as_tuple()[2]
    return str(normalized if exponent <= 0 else normalized.quantize(1))
