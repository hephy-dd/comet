import logging

__all__ = ['logger']

def setup():
    logger = logging.getLogger('comet')
    logger.setLevel(logging.INFO)

def logger():
    return logging.getLogger('comet')

setup()
