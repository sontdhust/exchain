"""
Config
"""

import os.path
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(sys.modules['__main__'].__file__))
CONFIG_FILE = os.path.join(ROOT_DIR, 'storage', 'config.json')

def read_config(key):
    """
    Read config
    """
    config = json.load(open(CONFIG_FILE))
    for sub_key in key.split('.'):
        config = config[sub_key]
    return config
