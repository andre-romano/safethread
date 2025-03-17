import time
import unittest

from safethread.thread import SchedulerThread, BaseThread


class TestSchedulerThread(unittest.TestCase):

    def _set_up_scheduler(self):
        # NON-REPEATED SCHEDULER
        self.scheduler_called = 0
        self.scheduler_result = 0

        def callback(x) -> bool:
            self.scheduler_called += 1
            self.scheduler_result = x+1
            return True

        self.scheduler = SchedulerThread(
            timeout=0.1,
            callback=callback,
            args=[1],
            repeat=False,
        )

    def _set_up_scheduler_rep(self):
        # REPEATED SCHEDULER
        self.scheduler_rep_called = 0
        self.scheduler_rep_result = 0

        def callback_two(a, b) -> bool:
            self.scheduler_rep_called += 1
            self.scheduler_rep_result += a+b
            if self.scheduler_rep_called == 2:
                return False
            return True

        self.scheduler_rep = SchedulerThread(
            timeout=0.1,
            callback=callback_two,
            args=[2, 3],
            repeat=True,
        )

    def setUp(self) -> None:
        self._set_up_scheduler()
        self._set_up_scheduler_rep()

    def test_invalid_callback(self):
        """Test that an exception is raised if the callback is not callable."""
        with self.assertRaises(TypeError):
            SchedulerThread(
                timeout=1.0,
                callback="not_a_function",  # type: ignore
                args=[1, 2]
            )

    def test_callback_execution(self):
        """Test that the callback is executed after the timeout."""

        # start scheduler
        begin = time.perf_counter()
        self.scheduler.start()

        # wait for scheduler to finish
        self.scheduler.join()
        end = time.perf_counter()

        self.assertTrue(self.scheduler.is_terminated())
        self.assertTrue(self.scheduler.get_timeout() == 0.1)
        self.assertTrue(self.scheduler_called == 1)
        self.assertTrue(self.scheduler_result == 2)

        self.assertTrue(
            end-begin >= self.scheduler.get_timeout())  # in secs

    def test_callback_repeat(self):
        """Test that the callback is executed repeatedly if repeat is True."""

        # Run repeatable scheduler
        self.scheduler_rep.start()

        # Let it run for a while
        self.scheduler_rep.join()

        # Check that the callback was called 2 times
        self.assertTrue(self.scheduler_rep_called == 2)
        self.assertTrue(self.scheduler_rep_result == 10)


if __name__ == '__main__':
    unittest.main()
