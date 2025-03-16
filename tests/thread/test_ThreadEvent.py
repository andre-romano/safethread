import unittest

import threading

from safethread.thread.ThreadEvent import ThreadEvent


class TestThreadEvent(unittest.TestCase):

    def setUp(self):
        self.event = ThreadEvent()

    def test_initial_state(self):
        self.assertFalse(self.event.is_set(),
                         "Event should not be set initially")

    def test_set_event(self):
        self.event.set()
        self.assertTrue(self.event.is_set(),
                        "Event should be set after calling set()")

    def test_thread_safety(self):
        def set_event():
            for _ in range(1000):
                self.event.set()

        threads = [threading.Thread(target=set_event) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertTrue(
            self.event.is_set(), "Event should be set after being set in multiple threads")


if __name__ == '__main__':
    unittest.main()
