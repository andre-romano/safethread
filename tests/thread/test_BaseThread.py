import unittest

import time

from safethread.thread import BaseThread


class TestBaseThread(unittest.TestCase):

    def _set_up_thread(self):
        def callback() -> bool:
            time.sleep(0.2)
            return True

        self.thread = BaseThread(
            callback=callback,
            daemon=True
        )

    def _set_up_thread_nd_repeat(self):
        self.thread_nd_repeat_called = 0
        self.thread_nd_repeat_result = 0

        def callback_two(a, b) -> bool:
            self.thread_nd_repeat_called += 1
            self.thread_nd_repeat_result += a+b

            if self.thread_nd_repeat_called == 2:
                return False  # interrupt thread now
            return True  # keep thread running

        self.thread_nd_repeat = BaseThread(
            callback=callback_two,
            args=[2, 3],
            daemon=False,
            repeat=True
        )

    def setUp(self) -> None:
        self._set_up_thread()
        self._set_up_thread_nd_repeat()

    def test_thread_start(self):
        self.assertFalse(self.thread.has_started())

        # Check if the thread is daemon
        self.assertTrue(self.thread.is_daemon())

        # The thread should not be terminated at first
        self.assertFalse(self.thread.is_terminated())

        # Start the thread
        self.thread.start()
        self.assertTrue(self.thread.has_started())

        # Check if the thread is alive
        self.assertTrue(self.thread.is_alive())

        # Check if the thread is repeatable
        self.assertFalse(self.thread.is_repeatable())

        # Wait for the thread to finish
        self.thread.join()

        # After join, the thread should not be alive
        self.assertFalse(self.thread.is_alive())

        # After the thread finishes, it should be terminated
        self.assertTrue(self.thread.is_terminated())

    def test_join_with_timeout(self):
        # Start the thread
        self.thread.start()

        # Join the thread with a timeout
        self.thread.join(timeout=0.1)

        # The join must timeout, in that case the thread is still running
        self.assertFalse(self.thread.is_terminated())

    def test_non_daemon_thread(self):
        # Check if the thread is daemon
        self.assertFalse(self.thread_nd_repeat.is_daemon())

        # set daemon
        self.thread_nd_repeat.set_daemon(True)

        # Check if the thread is daemon
        self.assertTrue(self.thread_nd_repeat.is_daemon())

        # Start the thread
        self.thread_nd_repeat.start()

        # Join the thread
        self.thread_nd_repeat.join()

        # Check that the callback was called 2 times
        self.assertTrue(self.thread_nd_repeat_called == 2)
        self.assertTrue(self.thread_nd_repeat_result == 10)


if __name__ == "__main__":
    unittest.main()
