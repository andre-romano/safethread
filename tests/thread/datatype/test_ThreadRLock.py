import unittest
import time

from threading import Thread

from safethread.thread.datatype.ThreadRLock import ThreadRLock


class TestThreadRLock(unittest.TestCase):

    def test_with_statement(self):
        lock = ThreadRLock()
        with lock:
            self.assertTrue(lock.acquire())
            lock.release()

    def test_release_not_locked(self):
        lock = ThreadRLock()
        with self.assertRaises(RuntimeError):
            lock.release()

    def test_acquire_release(self):
        lock = ThreadRLock()
        self.assertTrue(lock.acquire(blocking=False))
        lock.release()

        self.assertTrue(lock.acquire())
        self.assertTrue(lock.acquire())
        lock.release()
        lock.release()
        with self.assertRaises(RuntimeError):
            lock.release()

    def test_threading(self):
        lock = ThreadRLock()
        results = []

        def worker():
            with lock:
                results.append('locked')
                results.append('released')
                time.sleep(0.05)

        threads = [Thread(target=worker) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(results, ['locked', 'released']*5)

    def test_timeout(self):
        lock = ThreadRLock()
        timeout = 0.1

        def worker():
            with lock:
                time.sleep(timeout)

        begin = time.perf_counter()

        threads = [Thread(target=worker) for _ in range(1)]
        for thread in threads:
            thread.start()

        # Wait for the lock to be acquired by one of the worker processes
        time.sleep(0.05)  # Adjust this sleep time as needed

        with lock:
            self.assertGreaterEqual(time.perf_counter()-begin, timeout)

        for thread in threads:
            thread.join()

    def test_blocking(self):
        lock = ThreadRLock()
        timeout = 0.1

        def worker():
            with lock:
                time.sleep(timeout)

        threads = [Thread(target=worker) for _ in range(3)]
        for thread in threads:
            thread.start()

        self.assertFalse(lock.acquire(blocking=False))
        self.assertFalse(lock.acquire(blocking=False))

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    unittest.main()
