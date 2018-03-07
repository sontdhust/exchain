"""
Notification
"""

import json
import requests

def notify_trade(assets, side):
    """
    Notify trade
    """
    text = '\n'.join([(
        '*' + a['pair'].upper() + '* (_' + a['exchange'].title() + '_): ' + str(a['price']) + '.'
    ) for a in assets[1]])
    send_slack_message(assets[0], '', [{
        'fallback': side.title() + '.',
        'text': text,
        'color': 'warning' if 'close' in side else ('good' if 'buy' in side else 'danger'),
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
