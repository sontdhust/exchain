"""
Logger
"""

import os.path
from storage.config import ROOT_DIR

def write_log(file_name, text):
    """
    Write log
    """
    file_path = os.path.join(ROOT_DIR, 'storage', 'logs', file_name + '.log')
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'a') as log_file:
        log_file.write(str(text) + "\n")
