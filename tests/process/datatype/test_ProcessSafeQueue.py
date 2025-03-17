import time
import unittest
import multiprocessing

from safethread.process.datatype import ProcessRLock, ProcessSafeQueue


def worker(output: ProcessSafeQueue):
    output.put(42)


def producer(output: ProcessSafeQueue):
    for i in range(5):
        output.put(i)
        time.sleep(0.1)


def consumer(input: ProcessSafeQueue, output: ProcessSafeQueue):
    while True:
        try:
            output.put(input.get(timeout=1))
        except:
            break


class TestProcessSafeQueue(unittest.TestCase):

    def test_initialization_with_none(self):
        queue = ProcessSafeQueue()
        self.assertTrue(queue.maxsize == 0)
        self.assertTrue(queue._data.empty())

        self.assertIsInstance(queue._lock, ProcessRLock)

    def test_initialization_with_int(self):
        queue = ProcessSafeQueue(10)
        self.assertTrue(queue.maxsize == 10)
        self.assertTrue(queue._data.empty())

    def test_initialization_with_queue(self):
        initial_queue = multiprocessing.Queue()
        initial_queue.put(1)
        initial_queue.put(2)

        queue = ProcessSafeQueue(initial_queue)
        self.assertTrue(queue.maxsize == 0)
        self.assertFalse(queue._data.empty())
        self.assertTrue(queue._data.get() == 1)
        self.assertTrue(queue._data.get() == 2)

    def test_equality(self):
        queue1 = ProcessSafeQueue()
        queue2 = ProcessSafeQueue()
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue1 == queue2)

        queue1._data.put(1)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue1 != queue2)

        queue2._data.put(1)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue1 == queue2)

    def test_create_data_with_invalid_type(self):
        with self.assertRaises(TypeError):
            ProcessSafeQueue("invalid")  # type: ignore

    def test_multiprocessing_queue(self):
        queue = ProcessSafeQueue()
        process = multiprocessing.Process(target=worker, args=(queue,))
        process.start()
        process.join()

        self.assertFalse(queue.empty())
        self.assertEqual(queue.get(), 42)

    def test_multiprocessing_queue_get_blocking(self):
        queue = ProcessSafeQueue()
        process = multiprocessing.Process(target=worker, args=(queue,))
        process.start()

        self.assertEqual(queue.get(), 42)

        process.join()

    def test_parallel_put_get(self):
        queue = ProcessSafeQueue()
        results = ProcessSafeQueue()

        p1 = multiprocessing.Process(target=producer, args=(queue,))
        p2 = multiprocessing.Process(target=consumer, args=(queue, results))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])

    def test_shutdown(self):
        queue = ProcessSafeQueue()
        process = multiprocessing.Process(target=producer, args=(queue,))
        process.start()
        process.join()

        queue.shutdown()  # Shut down the queue
        self.assertTrue(True)

    def test_clear(self):
        queue = ProcessSafeQueue()
        for i in range(5):
            queue.put(i)

        self.assertFalse(queue.empty())
        queue.clear()
        self.assertTrue(queue.empty())


if __name__ == '__main__':
    unittest.main()
