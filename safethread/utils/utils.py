
"""Utility functions for the library"""

from typing import Callable, Iterable


def try_except_finally_wrap(callback: Callable, callback_fail: Callable = lambda: None, callback_final: Callable = lambda: None):
    """
    Wraps callback in a try except finally block

    Args:

        callback (Callable): Callable to wrap in try block

        callback_fail (Callable): Callable to run if except block is executed

        callback_final (Callable): Callable to run in finally block
    """
    try:
        callback()
    except:
        callback_fail()
    finally:
        callback_final()
