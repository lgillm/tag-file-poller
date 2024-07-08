import time
import logging
from loguru import logger
DEFAULT_FORMAT = 'Function: {name}: Process Time: {elapsed: 0.2f}s'


def clock(active: bool, output_format=DEFAULT_FORMAT):
    def decorate(func):
        def clocked(*_args):
            if active:
                start = time.perf_counter()
                _result = func(*_args)
                elapsed = time.perf_counter() - start
                name = func.__name__
                args = ', '.join(repr(arg) for arg in _args)
                result = repr(_result)
                logger.info(output_format.format(**locals()))

                return _result
        return clocked
    return decorate