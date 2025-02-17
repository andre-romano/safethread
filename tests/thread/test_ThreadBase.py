import unittest

from time import sleep

from safethread.thread import ThreadBase


class TestThreadBase(unittest.TestCase):

    class ConcreteThreadBase(ThreadBase):
        def __init__(self, args: list, daemon: bool = True):
            super().__init__(args, daemon)

        def _run(self, *args):
            """Override the _run method to simulate thread work."""
            sleep(0.2)  # Simulate some work

    def setUp(self) -> None:
        self.thread = TestThreadBase.ConcreteThreadBase(
            args=[], daemon=True)
        self.thread_ndaemon = TestThreadBase.ConcreteThreadBase(
            args=[], daemon=False)

    def test_thread_start(self):
        self.assertFalse(self.thread.has_started())

        # Start the thread
        self.thread.start()
        self.assertTrue(self.thread.has_started())

        # Check if the thread is alive
        self.assertTrue(self.thread.is_alive())

        # Wait for the thread to finish
        self.thread.join()

        # After join, the thread should not be alive
        self.assertFalse(self.thread.is_alive())

    def test_is_terminated(self):
        # The thread should not be terminated at first
        self.assertFalse(self.thread.is_terminated())

        # Start the thread and wait for it to finish
        self.thread.start()
        self.thread.join()

        # After the thread finishes, it should be terminated
        self.assertTrue(self.thread.is_terminated())

    def test_join_with_timeout(self):
        # Start the thread
        self.thread.start()

        # Join the thread with a timeout
        self.thread.join(timeout=0.1)

        # The join must timeout, in that case the thread is still running
        self.assertFalse(self.thread.is_terminated())

    def test_join_without_timeout(self):
        # Start the thread
        self.thread.start()

        # Join the thread without timeout
        self.thread.join()

        # After join, the thread should not be alive
        self.assertFalse(self.thread.is_alive())

    def test_non_daemon_thread(self):
        # Start the thread
        self.thread_ndaemon.start()

        # Check if the thread is daemon
        self.assertFalse(self.thread_ndaemon.is_daemon())

        # Join the thread
        self.thread_ndaemon.join()

    def test_daemon_thread(self):
        # Start the thread
        self.thread.start()

        # Check if the thread is daemon
        self.assertTrue(self.thread.is_daemon())

        # Join the thread
        self.thread.join()


if __name__ == "__main__":
    unittest.main()
