import functools
import logging

logging.getLogger().setLevel(logging.INFO)

def error_handler(func=None, *, default=None):
    def inner_function_wrapper(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                logging.error(f"{func.__name__}: {ex}")
                return default

        return inner_function

    if func:
        return inner_function_wrapper(func)
    else:
        return inner_function_wrapper
