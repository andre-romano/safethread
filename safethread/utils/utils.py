
"""Utility functions for the library"""

from typing import Callable, Iterable


def try_except_finally_wrap(
    callback: Callable,
    callback_succ: Callable = lambda: None,
    callback_fail: Callable = lambda: None,
    callback_final: Callable = lambda: None
):
    """
    Wraps a given callback function in a try-except-finally block.

    This utility function allows for the execution of a callback function with error
    handling and final actions. If an exception occurs during the execution of the 
    `callback`, the `callback_fail` function is called. If no exception occurs, the
    `callback_succ` function is called. Regardless of success or failure, 
    the `callback_final` function will always be executed in the finally block.

    :param callback: The function to be executed within the try block.
    :type callback: Callable

    :param callback_succ: The function to be executed if mo exception is raised.
    :type callback_succ: Callable, optional (defaults to a no-op lambda)

    :param callback_fail: The function to be executed if an exception is raised.
    :type callback_fail: Callable, optional (defaults to a no-op lambda)

    :param callback_final: The function to be executed in the finally block, regardless of success or failure.
    :type callback_final: Callable, optional (defaults to a no-op lambda)
    """
    try:
        callback()
        callback_succ()
    except:
        callback_fail()
    finally:
        callback_final()
