from multiprocessing.managers import ListProxy
import unittest

import multiprocessing
import threading

from safethread.utils import HybridRLock


def process_task(lock: HybridRLock, results: ListProxy):
    with lock:
        results.append(1)


def process_task_two(lock: HybridRLock, results: ListProxy):
    with lock:
        with lock:
            results.append(1)


class TestHybridRLock(unittest.TestCase):

    def setUp(self):
        self.lock = HybridRLock()

    def test_acquire_release(self):
        # Test acquiring and releasing the lock
        self.assertTrue(self.lock.acquire())
        self.lock.release()

    def test_thread_synchronization(self):
        # Test synchronization within a single process (threading)
        results = []

        def thread_task(lock: HybridRLock, results: list):
            with lock:
                results.append(1)

        threads = [threading.Thread(target=thread_task, args=(
            self.lock, results)) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(results), 10)
        self.assertEqual(results, [1]*10)

    def test_process_synchronization(self):
        # Test synchronization between different processes (multiprocessing)
        results = multiprocessing.Manager().list()

        processes = [multiprocessing.Process(
            target=process_task, args=(self.lock, results)) for _ in range(10)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

        self.assertEqual(len(results), 10)
        self.assertEqual(list(results), [1]*10)

    def test_process_synchronization_two(self):
        # Test synchronization between different processes (multiprocessing)
        results = multiprocessing.Manager().list()

        processes = [multiprocessing.Process(
            target=process_task_two, args=(self.lock, results)) for _ in range(10)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

        self.assertEqual(len(results), 10)
        self.assertEqual(list(results), [1]*10)

    def test_acquire_reentrant(self):
        self.assertTrue(self.lock.acquire())
        self.assertTrue(self.lock.acquire())
        self.lock.release()
        self.lock.release()

    def test_acquire_reentrant_two(self):
        with self.lock:
            with self.lock:
                self.assertEqual(True, True)

    def test_release_without_acquire(self):
        # Test releasing the lock without acquiring it first
        self.lock.release()


if __name__ == '__main__':
    unittest.main()
