"""
For measuring processing time
"""


import time
import logging
import functools

__author__ = 'damirah'
__email__ = 'damirah@live.com'


def timeit(func):
    """
    Measure time a function took to run.
    Got the function from StackOverflow:
    http://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.getLogger(__name__).debug('function [{}] finished in {} ms'
            .format(func.__name__, int(elapsed_time * 1000)))
    return wrapper_func
