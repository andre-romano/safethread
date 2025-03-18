import unittest
import threading

from queue import Queue

# Ensure SafeQueueThread is imported from the correct module
from safethread.thread.datatype import ThreadSafeQueue


class TestSafeThreadQueue(unittest.TestCase):

    def test_initialization_from_int(self):
        # Test that initializing SafeQueueThread with an integer sets the maxsize correctly
        queue_1 = ThreadSafeQueue(5)
        self.assertTrue(queue_1.maxsize == 5)
        self.assertTrue(queue_1.empty())

    def test_initialization_from_existing_queue(self):
        # Test that initializing SafeQueueThread with an existing Queue copies the data correctly
        original_queue = Queue()
        for i in range(5):
            original_queue.put(i)

        queue_1 = ThreadSafeQueue(original_queue)

        # Check if all items are copied correctly
        self.assertTrue(queue_1.qsize() == 5)

        # Ensure the original queue is empty after being copied
        self.assertTrue(original_queue.empty())

    def test_thread_safety(self):
        queue_1 = ThreadSafeQueue()

        def producer():
            for i in range(5):
                queue_1.put(i)

        def consumer():
            for i in range(5):
                queue_1.get()

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
        self.assertTrue(queue_1.qsize() == 0)
        # Ensure all tasks are done
        self.assertTrue(queue_1.all_tasks_done)

    def test_get_and_put(self):
        queue_1 = ThreadSafeQueue()

        # Test put() and get() methods
        queue_1.put(1)
        self.assertTrue(queue_1.get() == 1)

        # Test put_nowait() and get_nowait()
        queue_1.put_nowait(2)
        self.assertTrue(queue_1.get_nowait() == 2)

    def test_shutdown(self):
        queue_1 = ThreadSafeQueue()

        # Shutdown the queue and check its status
        queue_1.shutdown()
        self.assertTrue(queue_1.is_shutdown)

        # Test if 'put' and 'get' raise errors after shutdown
        # Assuming shutdown raises a general exception
        with self.assertRaises(Exception):
            queue_1.put(1)

        with self.assertRaises(Exception):
            queue_1.get()

    def test_task_done_and_unfinished_tasks(self):
        queue_1 = ThreadSafeQueue()

        # Test task_done() and unfinished_tasks()
        queue_1.put(1)
        queue_1.task_done()

        # Check if the unfinished tasks are updated
        self.assertTrue(queue_1.unfinished_tasks == 0)

        queue_1.put(2)
        self.assertTrue(queue_1.unfinished_tasks == 1)
        queue_1.task_done()
        self.assertTrue(queue_1.unfinished_tasks == 0)

    def test_empty_full_and_qsize(self):
        queue_1 = ThreadSafeQueue(3)

        self.assertTrue(queue_1.empty())
        self.assertFalse(queue_1.full())

        # Add items and check the size
        queue_1.put(1)
        self.assertTrue(queue_1.qsize() == 1)

        queue_1.put(2)
        queue_1.put(3)
        self.assertTrue(queue_1.qsize() == 3)
        self.assertTrue(queue_1.full())

        # Try adding one more item to a full queue
        # This will raise a queue.Full exception
        with self.assertRaises(Exception):
            queue_1.put(4, block=False)

    def test_clear(self):
        queue_1 = ThreadSafeQueue()

        # Add items to the queue
        queue_1.put(1)
        queue_1.put(2)

        # Clear the queue
        queue_1.clear()  # Directly clear the underlying queue

        # Test if the queue is empty after clearing
        self.assertTrue(queue_1.empty())

    def test_parallel_put_get(self):
        queue_1 = ThreadSafeQueue()
        results = ThreadSafeQueue()

        def producer(output: ThreadSafeQueue):
            for i in range(5):
                output.put(i)

        def consumer(input: ThreadSafeQueue, output: ThreadSafeQueue):
            while True:
                try:
                    output.put(input.get(timeout=1))
                except:
                    break

        p1 = threading.Thread(target=producer, args=(queue_1,))
        p2 = threading.Thread(target=consumer, args=(queue_1, results))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
