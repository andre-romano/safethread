import logging

import multiprocessing
import threading

from typing import Self


class HybridRLock:
    """
    A lock class that supports both inter-process (multiprocessing) and
    intra-process (threading) synchronization.

    - Uses `multiprocessing.RLock` to synchronize access between different processes.
    - Uses `threading.RLock` to synchronize access within a single process.
    """

    def __init__(self):
        # Lock for inter-process synchronization
        self.__mp_lock = multiprocessing.RLock()
        # Lock for intra-process synchronization
        self.__thread_lock = threading.RLock()

    def __getstate__(self):
        """
        Return state for pickling. Exclude the threading.RLock as it cannot be pickled.
        """
        state = self.__dict__.copy()
        # Remove the threading.RLock from the state
        del state["_HybridRLock__thread_lock"]
        return state

    def __setstate__(self, state):
        """
        Restore state after unpickling. Reinitialize the threading.RLock.
        """
        self.__dict__.update(state)
        self.__thread_lock = threading.RLock()  # Reinitialize the threading.RLock

    def acquire(self) -> bool:
        """
        Acquire both threading and multiprocess RLocks.

        This operation is BLOCKING.

        :return: True if both locks were acquired, False otherwise.
        :rtype: bool
        """
        acquired_mp = False
        acquired_thread = False

        try:
            acquired_mp = self.__mp_lock.acquire()
            if not acquired_mp:
                return False

            acquired_thread = self.__thread_lock.acquire()
            if not acquired_thread:
                self.__mp_lock.release()  # Release `_mp_lock` if `_thread_lock` acquisition fails
                return False

            return True  # Successfully acquired both locks

        except Exception as e:
            if acquired_thread:  # Ensure we only release if `_thread_lock` was actually acquired
                self.__thread_lock.release()
            if acquired_mp:  # Ensure we only release if `_mp_lock` was actually acquired
                self.__mp_lock.release()
            logging.error(f"HybridRLock acquisition failed: {e}")
            return False

    def release(self):
        """
        Release the locks.
        """

        try:
            self.__thread_lock.release()  # Release thread lock first
        except Exception as e:
            pass

        try:
            self.__mp_lock.release()  # Release process lock
        except Exception as e:
            pass

    def __enter__(self) -> Self:
        """
        Enter the context manager (automatically acquire the lock).
        """
        self.acquire()
        return self

    def __exit__(self, *args):
        """
        Exit the context manager (automatically release the lock).
        """
        self.release()
