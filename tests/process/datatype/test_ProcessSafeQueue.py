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
        queue_1 = ProcessSafeQueue()
        self.assertTrue(queue_1.maxsize == 0)
        self.assertTrue(queue_1.empty())

        self.assertIsInstance(queue_1._lock, ProcessRLock)

    def test_initialization_with_int(self):
        queue_1 = ProcessSafeQueue(10)
        self.assertTrue(queue_1.maxsize == 10)
        self.assertTrue(queue_1.empty())

    def test_initialization_with_queue(self):
        initial_queue = multiprocessing.Queue()
        initial_queue.put(1)
        initial_queue.put(2)

        queue = ProcessSafeQueue(initial_queue)
        self.assertTrue(queue.get() == 1)
        self.assertTrue(queue.qsize() == 1)
        self.assertFalse(queue.empty())
        self.assertFalse(queue.full())
        self.assertTrue(queue.maxsize == 0)

        self.assertTrue(queue.get() == 2)
        self.assertTrue(queue.qsize() == 0)
        self.assertTrue(queue.empty())
        self.assertFalse(queue.full())
        self.assertTrue(queue.maxsize == 0)

    def test_equality(self):
        queue_1 = ProcessSafeQueue()
        queue_2 = ProcessSafeQueue()
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue_1 == queue_2)

        queue_1.put(1)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue_1 != queue_2)

        queue_2.put(1)
        with self.assertRaises(NotImplementedError):
            self.assertTrue(queue_1 == queue_2)

    def test_create_data_with_invalid_type(self):
        with self.assertRaises(TypeError):
            ProcessSafeQueue("invalid")  # type: ignore

    def test_multiprocessing_queue(self):
        queue_1 = ProcessSafeQueue()
        process = multiprocessing.Process(target=worker, args=(queue_1,))
        process.start()
        process.join()

        self.assertFalse(queue_1.empty())
        self.assertEqual(queue_1.get(), 42)

    def test_multiprocessing_queue_get_blocking(self):
        queue_1 = ProcessSafeQueue()
        process = multiprocessing.Process(target=worker, args=(queue_1,))
        process.start()

        self.assertEqual(queue_1.get(), 42)

        process.join()

    def test_parallel_put_get(self):
        queue_1 = ProcessSafeQueue()
        results = ProcessSafeQueue()

        p1 = multiprocessing.Process(target=producer, args=(queue_1,))
        p2 = multiprocessing.Process(target=consumer, args=(queue_1, results))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])

    def test_shutdown(self):
        queue_1 = ProcessSafeQueue()
        process = multiprocessing.Process(target=producer, args=(queue_1,))
        process.start()
        process.join()

        queue_1.shutdown()  # Shut down the queue_1
        self.assertTrue(True)

    def test_clear(self):
        queue_1 = ProcessSafeQueue()
        for i in range(5):
            queue_1.put(i)

        time.sleep(0.05)

        self.assertFalse(queue_1.full())
        self.assertFalse(queue_1.empty())

        queue_1.clear()
        time.sleep(0.05)

        self.assertFalse(queue_1.full())
        self.assertTrue(queue_1.empty())


if __name__ == '__main__':
    unittest.main()
