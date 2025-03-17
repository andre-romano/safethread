import unittest
import threading
import time

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

    def test_clear_event(self):
        self.event.set()
        self.event.clear()
        self.assertFalse(self.event.is_set(),
                         "Event should not be set after calling clear()")

    def test_wait_for_event(self):
        def set_event():
            time.sleep(0.1)
            self.event.set()

        threading.Thread(target=set_event).start()
        self.assertTrue(self.event.wait(timeout=1),
                        "Event should be set within the timeout period")

    def test_thread_safety_set(self):
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

    def test_thread_safety_clear(self):
        self.event.set()

        def clear_event():
            for _ in range(1000):
                self.event.clear()

        threads = [threading.Thread(target=clear_event) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertFalse(
            self.event.is_set(), "Event should not be set after being cleared in multiple threads")


if __name__ == '__main__':
    unittest.main()
