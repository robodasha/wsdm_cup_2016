"""
Utilities for logging
"""

import os
import json
import math
import logging
import logging.config

from wsdmcup.config import Config

__author__ = 'damirah'
__email__ = 'damirah@live.com'


def setup_logging(default_path='logging.json', default_level=logging.DEBUG):
    """
    Setup logging configuration
    :param default_path:
    :param default_level:
    :return: None
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        config['handlers']['file']['filename'] = \
            Config.get_path_to_log_file('debug.log')
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    return


def get_total(file_path):
    """
    Count number of lines in file, useful when processing very large files
    (to be able to report on progress)
    :param file_path: path to file
    :return: number of lines in the file
    """
    with open(file_path, 'r') as f:
        num_lines = sum(1 for line in f)
    return num_lines


def how_often(total, update_freq=100):
    """
    :param total: how many items in total have to be processed
    :param update_freq: default is 100, that is -- update every 1%
    :return: number denoting after how many items should progress be updated
    """
    return math.ceil(total / update_freq)


def get_progress(processed, total):
    """
    Based on how many items were processed and how many items are there in total
    return string representing progress (e.g. "Progress: 54%")
    :param processed: number of already processed items
    :param total: total number of items to be processed
    :return: string with current progress
    """
    progress = processed / total * 100
    return "Progress: %.2f%%" % round(progress, 2)
