import unittest
import time

import multiprocessing
import multiprocessing.synchronize

from multiprocessing import Process, Value
from multiprocessing.managers import ListProxy
from multiprocessing.sharedctypes import Synchronized

from safethread.process.datatype import ProcessRLock


def worker_multiprocessing(lock: ProcessRLock, results: ListProxy):
    with lock:
        results.append('locked')
        time.sleep(0.1)
        results.append('released')


def worker_timeout(lock: ProcessRLock, timeout: float, ready_event: multiprocessing.synchronize.Event):
    with lock:
        ready_event.set()  # Signal that the lock has been acquired
        time.sleep(timeout)


class TestProcessRLock(unittest.TestCase):

    def test_with_statement(self):
        lock = ProcessRLock()
        with lock:
            self.assertTrue(lock.acquire())
            lock.release()

    def test_release_not_locked(self):
        lock = ProcessRLock()
        with self.assertRaises(RuntimeError):
            lock.release()

    def test_acquire_release(self):
        lock = ProcessRLock()
        self.assertTrue(lock.acquire(blocking=False))
        lock.release()

        self.assertTrue(lock.acquire())
        self.assertTrue(lock.acquire())
        lock.release()
        lock.release()
        with self.assertRaises(RuntimeError):
            lock.release()

    def test_multiprocessing(self):
        lock = ProcessRLock()
        results = multiprocessing.Manager().list()

        processes = [
            Process(
                target=worker_multiprocessing,
                args=[lock, results]
            ) for _ in range(5)
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

        self.assertEqual(list(results), ['locked', 'released']*5)

    def test_timeout(self):
        lock = ProcessRLock()
        timeout = 0.1
        ready_event = multiprocessing.Event()

        processes = [
            Process(
                target=worker_timeout,
                args=[lock, timeout, ready_event]
            ) for _ in range(5)
        ]

        begin = time.perf_counter()
        for process in processes:
            process.start()

        # Wait for at least one worker process to acquire the lock
        ready_event.wait()

        with lock:
            self.assertGreaterEqual(time.perf_counter()-begin, timeout)

        for process in processes:
            process.join()

    def test_blocking(self):
        lock = ProcessRLock()
        timeout = 0.1
        ready_event = multiprocessing.Event()

        processes = [
            Process(
                target=worker_timeout,
                args=[lock, timeout, ready_event]
            ) for _ in range(3)
        ]

        for process in processes:
            process.start()

        # Wait for at least one worker process to acquire the lock
        ready_event.wait()

        self.assertFalse(lock.acquire(blocking=False))
        self.assertFalse(lock.acquire(blocking=False))

        for process in processes:
            process.join()


if __name__ == '__main__':
    unittest.main()
