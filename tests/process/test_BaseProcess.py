import unittest

import time

from multiprocessing import Value
from multiprocessing.sharedctypes import Synchronized

from safethread.process import BaseProcess


def callback():
    time.sleep(0.2)
    return True


def callback_two(repeat_called: Synchronized, repeat_result: Synchronized, a: int, b: int):
    with repeat_called.get_lock(), repeat_result.get_lock():  # Ensure process-safety
        repeat_called.value += 1
        repeat_result.value += a+b
        if repeat_called.value == 2:
            return False  # terminate process loop
        return True


class TestBaseProcess(unittest.TestCase):
    def setUp(self) -> None:

        self.process_nd_repeat_called = Value("i", 0)
        self.process_nd_repeat_result = Value("i", 0)

        self.process = BaseProcess(
            callback=callback,
            daemon=True)

        self.process_nd_repeat = BaseProcess(
            callback=callback_two,
            args=[
                self.process_nd_repeat_called,
                self.process_nd_repeat_result,
                2,
                3,
            ], daemon=False, repeat=True)

    def test_process_start(self):
        self.assertFalse(self.process.has_started())

        # Check if the process is daemon
        self.assertTrue(self.process.is_daemon())

        # The process should not be terminated at first
        self.assertFalse(self.process.is_terminated())

        # Start the process
        self.process.start()
        self.assertTrue(self.process.has_started())

        # Check if the process is alive
        self.assertTrue(self.process.is_alive())

        # Check if the process is repeatable
        self.assertFalse(self.process.is_repeatable())

        # Wait for the process to finish
        self.process.join()

        # After join, the process should not be alive
        self.assertFalse(self.process.is_alive())

        # After the process finishes, it should be terminated
        self.assertTrue(self.process.is_terminated())

    def test_join_with_timeout(self):
        # Start the process
        self.process.start()

        # Join the process with a timeout
        self.process.join(timeout=0.1)

        # The join must timeout, in that case the process is still running
        self.assertFalse(self.process.is_terminated())

    def test_process_start_stop(self):
        # Start the process
        self.process_nd_repeat.start()
        self.process_nd_repeat.stop()

        # Check if the process is repeatable
        self.assertTrue(self.process_nd_repeat.is_repeatable())

        # Wait for the process to finish
        self.process_nd_repeat.join()

        # Check that the callback was called 0 times
        with self.process_nd_repeat_called.get_lock():
            self.assertTrue(self.process_nd_repeat_called.value == 0)

        # Check that the callback result
        with self.process_nd_repeat_result.get_lock():
            self.assertTrue(self.process_nd_repeat_result.value == 0)

    def test_non_daemon_process(self):
        # Check if the process is daemon
        self.assertFalse(self.process_nd_repeat.is_daemon())

        # set daemon
        self.process_nd_repeat.set_daemon(True)

        # Check if the process is daemon
        self.assertTrue(self.process_nd_repeat.is_daemon())

        # Start the process
        self.process_nd_repeat.start()

        # Join the process
        self.process_nd_repeat.join()

        # Check that the callback was called 2 times
        with self.process_nd_repeat_called.get_lock():
            self.assertTrue(self.process_nd_repeat_called.value, 2)

        # Check that the callback result
        with self.process_nd_repeat_result.get_lock():
            self.assertTrue(self.process_nd_repeat_result.value, 10)


if __name__ == "__main__":
    unittest.main()
