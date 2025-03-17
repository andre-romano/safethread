import unittest
import multiprocessing

from safethread.process import ProcessEvent


def set_event(event: ProcessEvent):
    event.set()


class TestProcessEvent(unittest.TestCase):

    def test_event_initially_unset(self):
        event = ProcessEvent()
        self.assertFalse(event.is_set(), "Event should be initially unset")

    def test_set_event(self):
        event = ProcessEvent()
        event.set()
        self.assertTrue(event.is_set(), "Event should be set")

    def test_clear_event(self):
        event = ProcessEvent()
        event.set()
        event.clear()
        self.assertFalse(event.is_set(), "Event should be cleared")

    def test_wait_event(self):
        event = ProcessEvent()

        process = multiprocessing.Process(
            target=set_event, args=(event,))
        process.start()

        self.assertTrue(event.wait(timeout=1),
                        "Event should be set after delay")

        process.join()


if __name__ == '__main__':
    unittest.main()
