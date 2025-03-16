import logging
import time
import unittest

from multiprocessing import Value
from multiprocessing.sharedctypes import Synchronized

from safethread.process import SchedulerProcess, BaseProcess

scheduler_called: Synchronized
scheduler_result: Synchronized
scheduler: SchedulerProcess

scheduler_rep_called: Synchronized
scheduler_rep_result: Synchronized
scheduler_rep: SchedulerProcess


def callback(scheduler_called: Synchronized, scheduler_result: Synchronized, x: int) -> bool:
    with scheduler_called.get_lock(), scheduler_result.get_lock():
        scheduler_called.value += 1
        scheduler_result.value = x+1
        logging.debug("RUNNED CALLBACK")
        return True


def callback_two(scheduler_rep_called: Synchronized, scheduler_rep_result: Synchronized, a: int, b: int) -> bool:
    with scheduler_rep_called.get_lock(), scheduler_rep_result.get_lock():
        scheduler_rep_called.value += 1
        scheduler_rep_result.value += a+b
        logging.debug("RUNNED CALLBACK TWO")
        if scheduler_rep_called.value == 2:
            return False
        return True


def _set_up_scheduler():
    global scheduler_called, scheduler_result, scheduler

    # NON-REPEATED SCHEDULER
    scheduler_called = Value("i", 0)
    scheduler_result = Value("i", 0)

    scheduler = SchedulerProcess(
        timeout=0.1,
        callback=callback,
        args=[
            scheduler_called,
            scheduler_result,
            1,
        ],
        repeat=False,
    )


def _set_up_scheduler_rep():
    global scheduler_rep_called, scheduler_rep_result, scheduler_rep

    # REPEATED SCHEDULER
    scheduler_rep_called = Value("i", 0)
    scheduler_rep_result = Value("i", 0)

    scheduler_rep = SchedulerProcess(
        timeout=0.1,
        callback=callback_two,
        args=[
            scheduler_rep_called,
            scheduler_rep_result,
            2,
            3,
        ],
        repeat=True,
    )


class TestSchedulerProcess(unittest.TestCase):

    def setUp(self) -> None:
        _set_up_scheduler()
        _set_up_scheduler_rep()

    def test_invalid_callback(self):
        """Test that an exception is raised if the callback is not callable."""
        global scheduler_called, scheduler_result, scheduler
        global scheduler_rep_called, scheduler_rep_result, scheduler_rep

        with self.assertRaises(TypeError):
            SchedulerProcess(
                timeout=1.0,
                callback="not_a_function",  # type: ignore
                args=[1, 2]
            )

    def test_callback_execution(self):
        """Test that the callback is executed after the timeout."""
        global scheduler_called, scheduler_result, scheduler
        global scheduler_rep_called, scheduler_rep_result, scheduler_rep

        # start scheduler
        begin = time.perf_counter()
        scheduler.start()

        # wait for scheduler to finish
        scheduler.join()
        end = time.perf_counter()

        self.assertGreaterEqual(
            end-begin, scheduler.get_timeout())  # in secs

        self.assertEqual(scheduler.get_timeout(), 0.1)
        self.assertTrue(scheduler.is_terminated())

        with scheduler_result.get_lock(), scheduler_called.get_lock():
            self.assertEqual(scheduler_result.value, 2)
            self.assertEqual(scheduler_called.value, 1)

    def test_callback_repeat(self):
        """Test that the callback is executed repeatedly if repeat is True."""
        global scheduler_called, scheduler_result, scheduler
        global scheduler_rep_called, scheduler_rep_result, scheduler_rep

        # Run repeatable scheduler
        scheduler_rep.start()

        # Let it run for a while
        scheduler_rep.join()

        # Check that the callback was called 2 times
        with scheduler_rep_result.get_lock(), scheduler_rep_called.get_lock():
            self.assertEqual(scheduler_rep_called.value, 2)
            self.assertEqual(scheduler_rep_result.value, 10)


if __name__ == '__main__':
    unittest.main()
