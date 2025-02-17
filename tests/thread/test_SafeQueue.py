import unittest
import threading

from queue import Queue

# Ensure SafeQueue is imported from the correct module
from safethread.thread import SafeQueue


class TestSafeQueue(unittest.TestCase):

    def test_initialization_from_int(self):
        # Test that initializing SafeQueue with an integer sets the maxsize correctly
        safe_queue = SafeQueue(5)
        self.assertEqual(safe_queue.maxsize, 5)
        self.assertTrue(safe_queue.empty())

    def test_initialization_from_existing_queue(self):
        # Test that initializing SafeQueue with an existing Queue copies the data correctly
        original_queue = Queue()
        for i in range(5):
            original_queue.put(i)

        safe_queue = SafeQueue(original_queue)

        # Check if all items are copied correctly
        self.assertEqual(safe_queue.qsize(), 5)

        # Ensure the original queue is empty after being copied
        self.assertTrue(original_queue.empty())

    def test_thread_safety(self):
        safe_queue = SafeQueue()

        def producer():
            for i in range(5):
                safe_queue.put(i)

        def consumer():
            for i in range(5):
                safe_queue.get()

        threads = []
        for _ in range(3):
            t = threading.Thread(target=producer)
            threads.append(t)
            t.start()

        for _ in range(3):
            t = threading.Thread(target=consumer)
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Test that the queue is empty after all operations
        self.assertEqual(safe_queue.qsize(), 0)
        # Ensure all tasks are done
        self.assertTrue(safe_queue.all_tasks_done)

    def test_get_and_put(self):
        safe_queue = SafeQueue()

        # Test put() and get() methods
        safe_queue.put(1)
        self.assertEqual(safe_queue.get(), 1)

        # Test put_nowait() and get_nowait()
        safe_queue.put_nowait(2)
        self.assertEqual(safe_queue.get_nowait(), 2)

    def test_shutdown(self):
        safe_queue = SafeQueue()

        # Shutdown the queue and check its status
        safe_queue.shutdown()
        self.assertTrue(safe_queue.is_shutdown)

        # Test if 'put' and 'get' raise errors after shutdown
        # Assuming shutdown raises a general exception
        with self.assertRaises(Exception):
            safe_queue.put(1)

        with self.assertRaises(Exception):
            safe_queue.get()

    def test_task_done_and_unfinished_tasks(self):
        safe_queue = SafeQueue()

        # Test task_done() and unfinished_tasks()
        safe_queue.put(1)
        safe_queue.task_done()

        # Check if the unfinished tasks are updated
        self.assertEqual(safe_queue.unfinished_tasks, 0)

        safe_queue.put(2)
        self.assertEqual(safe_queue.unfinished_tasks, 1)
        safe_queue.task_done()
        self.assertEqual(safe_queue.unfinished_tasks, 0)

    def test_empty_full_and_qsize(self):
        safe_queue = SafeQueue(3)

        self.assertTrue(safe_queue.empty())
        self.assertFalse(safe_queue.full())

        # Add items and check the size
        safe_queue.put(1)
        self.assertEqual(safe_queue.qsize(), 1)

        safe_queue.put(2)
        safe_queue.put(3)
        self.assertEqual(safe_queue.qsize(), 3)
        self.assertTrue(safe_queue.full())

        # Try adding one more item to a full queue
        # This will raise a queue.Full exception
        with self.assertRaises(Exception):
            safe_queue.put(4, block=False)

    def test_clear(self):
        safe_queue = SafeQueue()

        # Add items to the queue
        safe_queue.put(1)
        safe_queue.put(2)

        # Clear the queue
        safe_queue.queue.clear()  # Directly clear the underlying queue

        # Test if the queue is empty after clearing
        self.assertTrue(safe_queue.empty())


if __name__ == '__main__':
    unittest.main()
