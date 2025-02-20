
import queue

from typing import Any, Callable, Iterable, Self, Type

from .utils import *

from ..thread.ThreadBase import ThreadBase


class PipelineStage:
    """
    A pipeline stage that processes data through a callback function.
    It can run N separate threads to read and write data in parallel.

    This class allows data to be pushed to an input queue, where it is processed
    by the provided callback function, and the result is then placed in an output
    queue. This can be useful for concurrent processing of tasks in a pipeline
    fashion.

    The pipeline runs indefinetely, until .stop() is called.

    Args:

        callback (Callable): The function (or callable) that processes input data
                              and produces output. The callback should accept one
                              argument and return the processed result.

    Raises:

        ThreadBase.CallableException: If the provided callback is not callable.

        ValueError: If `n_threads` < 1.
    """

    EmptyException = queue.Empty
    """
    Raised when one of the following conditions happens:
    - get(block=False) is called, and there is no input in IN_QUEUE
    - get(timeout=value) and timeout exceeded (no input received within timeout time frame)
    """

    FullException = queue.Full
    """
    Raised when one of the following conditions happens:
    - put(block=False) is called and there is no available space in the OUT_QUEUE
    - put(timeout=value) and timeout exceeded (OUT_QUEUE full and timeout has expired)
    """

    StoppedException = queue.ShutDown
    """Raised when put()/get() is called after Pipeline.stop()"""

    @staticmethod
    def is_instance(obj: Any):
        """
        Checks if obj is an instance of PipelineStage

        Args:

            obj (Any): Object to check

        Raises:

            TypeError: if obj is not an instance of PipelineStage

        Returns:

            PipelineStage: object
        """
        if not isinstance(obj, PipelineStage):
            raise TypeError("Object is not a Pipeline Stage.")
        return obj

    def __init__(self, callback: Callable, n_threads: int = 1):
        """
        Initializes the pipeline stage with a callback function.

        Args:

            callback (Callable): The function to process data through the pipeline stage.
            n_threads (int): Number of threads that will read the input queue, and store result in output queue.

        Raises:

            ThreadBase.CallableException: If the callback argument is not callable.
            ValueError: If `n_threads` < 1.
        """

        self.__callback: Callable = ThreadBase.is_callable(callback)
        self.__input_queue = queue.Queue()
        self.__output_queue = queue.Queue()
        self.__started = False
        self.__threads: list[ThreadBase] = []

        if n_threads < 1:
            raise ValueError(
                "At least one thread is needed to run PipelineStage")

        for i in range(n_threads):
            self.__threads.append(
                ThreadBase(self.__run_pipeline, repeat=True)
            )

    def __run_pipeline(self):
        """
        Method to be executed in the thread. It gets data from the input queue,
        processes it through the callback function, and puts the result into
        the output queue.

        Raises:

            queue.Full: If the output queue is full (no available slot to store output)

        """
        try:
            input_data = self.__input_queue.get()
            output_data = self.__callback(input_data)
            self.__output_queue.put(output_data)
        except queue.ShutDown as e:
            self.stop()

    def has_started(self) -> bool:
        """
        Checks if the pipeline stage has started.

        Returns:

            bool: True if pipeline stage has started, otherwise False.
        """
        return self.__started

    def is_alive(self) -> bool:
        """
        Checks if the pipeline stage is alive.

        Returns:

            bool: True if any thread of pipeline stage is still alive, otherwise False.
        """
        result = False
        for thread in self.__threads:
            result = result or thread.is_alive()
        return result

    def is_terminated(self) -> bool:
        """
        Checks if the pipeline stage has terminated.

        Returns:

            bool: True if pipeline stage HAS started and is NOT alive, otherwise False.
        """
        return self.has_started() and not self.is_alive()

    def put(self, value, block: bool = True, timeout: float | None = None):
        """
        Puts data into the input queue for processing.

        Args:

            value (Any): The data to be processed by the pipeline.

            block (true): Block until data can be inserted in queue

            timeout (float, optional): Timeout for the put operation.

        Raises:

            FullException: if block = True and timeout is exceeded, or
                if block = False and there is no available space in the IN queue

            StoppedException: if pipeline has stopped
        """
        self.__input_queue.put(value, block, timeout)

    def get(self, block: bool = True, timeout: float | None = None):
        """
        Retrieves the processed data from the output queue.

        Args:

            block (true): Block until data can be get from queue

            timeout (float, optional): Timeout for the get operation.

        Returns:

            Any: The processed data after passing through the callback function.

        Raises:

            EmptyException: if block = True and timeout is exceeded, or
                if block = False and no output is available in the OUT queue
        """
        return self.__output_queue.get(block, timeout)

    def connect_output(self, other_pipeline: Self):
        """
        Connects this Pipeline Stage output to the input of other_pipeline

        Args:

            other_pipeline (Self): other pipeline stage
        """
        self.__output_queue = other_pipeline.__input_queue

    def start(self):
        """
        Starts the pipeline stage threads

        Raises:
            RuntimeError: if start() is called more than once on the same thread object.
        """
        for thread in self.__threads:
            thread.start()
        self.__started = True

    def stop(self):
        """
        Stops the pipeline thread (immediately)
        """
        # stops threads' main loops
        for thread in self.__threads:
            try_except_finally_wrap(lambda: thread.stop())
        # prevent in/out queues from storing data
        try_except_finally_wrap(
            lambda: self.__input_queue.shutdown(immediate=True)
        )
        try_except_finally_wrap(
            lambda: self.__output_queue.shutdown(immediate=True)
        )

    def join(self, timeout: float | None = None):
        """
        Joins the pipeline stages' threads, waiting for them to finish.

        Args:

            timeout (float, optional): The maximum time to wait for threads to finish. Defaults to None.

        Raises:

            RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        for thread in self.__threads:
            thread.join(timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the PipelineStage and waiting for its threads to finish.

        Args:

            timeout (float, optional): The maximum time to wait for threads to finish. Defaults to None.

        Raises:

            RuntimeError: if an attempt is made to join the current thread (main thread), or the join() is called before start()
        """
        self.stop()
        self.join(timeout=timeout)
