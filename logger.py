import logging
from functools import wraps

"""
This module is used to log the information of the functions and classes.
The log_config function is used to configure the logger with the default level.
The debug function is used to configure the logger with the DEBUG level.

It uses the decorator pattern to log the information of the functions.
We just need to add the @log_write or @log_debug decorator to the function,
and return the message we want to log.
"""


def log_config():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def debug():
    logger = logging.getLogger("debug")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


LOG = log_config()

DEBUG_LOG = debug()


def log_write(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f"{func.__name__} - "
        obj_name = args[0].__class__.__name__
        result = func(*args, **kwargs)
        LOG.info(result)
        return result

    return wrapper


def log_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f"{func.__name__} - "
        obj_name = args[0].__class__.__name__
        result = func(*args, **kwargs)
        DEBUG_LOG.debug(obj_name)
        DEBUG_LOG.debug(func_name)
        DEBUG_LOG.debug(result)
        return result

    return wrapper
