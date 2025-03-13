
import queue

from typing import Any, Callable, Self

from ...utils.utils import *

from ..BaseThread import BaseThread


class PipelineStageThreaded:
    """
    A pipeline stage that processes data through a callback function.
    It can run N separate threads to read and write data concurrently.

    This class allows data to be pushed to an input queue, where it is processed
    by the provided callback function, and the result is then placed in an output
    queue. This can be useful for concurrent processing of tasks in a pipeline
    fashion.

    The pipeline runs indefinitely until :meth:`stop()` is called.

    :param callback: The function (or callable) that processes input data and 
                     produces output. The callback should accept one argument 
                     and return the processed result.
    :type callback: Callable

    :raises ThreadBase.CallableException: If the provided callback is not callable.
    :raises ValueError: If `n_threads` is less than 1.

    <img src="../../../img/utils/PipelineStage.svg" alt="" width="100%">
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
        Checks if the object is an instance of PipelineStage.

        :param obj: The object to check.
        :type obj: Any

        :raises TypeError: If the object is not an instance of PipelineStage.

        :return: The PipelineStage object if it is an instance.
        :rtype: PipelineStage
        """
        if not isinstance(obj, PipelineStageThreaded):
            raise TypeError("Object is not a Pipeline Stage.")
        return obj

    def __init__(self, callback: Callable, n_threads: int = 1):
        """
        Initializes the pipeline stage with a callback function.

        :param callback: The function to process data through the pipeline stage.
        :type callback: Callable
        :param n_threads: Number of threads that will read the input queue, and 
                          store result in the output queue. Defaults to 1.
        :type n_threads: int

        :raises ThreadBase.CallableException: If the callback argument is not callable.
        :raises ValueError: If `n_threads` is less than 1.
        """

        self.__callback: Callable = BaseThread.is_callable(callback)
        self.__input_queue = queue.Queue()
        self.__output_queue = queue.Queue()
        self.__started = False
        self.__threads: list[BaseThread] = []

        if n_threads < 1:
            raise ValueError(
                "At least one thread is needed to run PipelineStage")

        for i in range(n_threads):
            self.__threads.append(
                BaseThread(self.__run_pipeline, repeat=True)
            )

    def __run_pipeline(self):
        """
        Method to be executed in the thread. It gets data from the input queue,
        processes it through the callback function, and puts the result into
        the output queue.

        :raises PipelineStage.FullException: If the output queue is full (no available slot to store output).
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

        :return: True if the pipeline stage has started, otherwise False.
        :rtype: bool
        """
        return self.__started

    def is_alive(self) -> bool:
        """
        Checks if the pipeline stage is alive.

        :return: True if any thread of the pipeline stage is still alive, otherwise False.
        :rtype: bool
        """
        result = False
        for thread in self.__threads:
            result = result or thread.is_alive()
        return result

    def is_terminated(self) -> bool:
        """
        Checks if the pipeline stage has terminated.

        :return: True if the pipeline stage has started and is not alive, otherwise False.
        :rtype: bool
        """
        return self.has_started() and not self.is_alive()

    def put(self, value, block: bool = True, timeout: float | None = None):
        """
        Puts data into the input queue for processing.

        :param value: The data to be processed by the pipeline.
        :type value: Any
        :param block: If True, block until data can be inserted into the queue. Defaults to True.
        :type block: bool, optional
        :param timeout: Timeout for the put operation. Defaults to None.
        :type timeout: float or None, optional

        :raises FullException: If block is True and the timeout is exceeded, or if block is False and 
                               there is no available space in the input queue.
        :raises StoppedException: If the pipeline has stopped.
        """
        self.__input_queue.put(value, block, timeout)

    def get(self, block: bool = True, timeout: float | None = None):
        """
        Retrieves the processed data from the output queue.

        :param block: If True, block until data can be retrieved from the queue. Defaults to True.
        :type block: bool, optional
        :param timeout: Timeout for the get operation. Defaults to None.
        :type timeout: float or None, optional

        :return: The processed data after passing through the callback function.
        :rtype: Any

        :raises EmptyException: If block is True and the timeout is exceeded, or if block is False and 
                                no output is available in the output queue.
        """
        return self.__output_queue.get(block, timeout)

    def connect_output(self, other_pipeline: Self):
        """
        Connects this Pipeline Stage output to the input of another pipeline.

        :param other_pipeline: Another pipeline stage.
        :type other_pipeline: Self
        """
        self.__output_queue = other_pipeline.__input_queue

    def start(self):
        """
        Starts the pipeline stage threads.

        :raises RuntimeError: If start() is called more than once on the same thread object.
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

        :param timeout: The maximum time to wait for threads to finish. Defaults to None.
        :type timeout: float or None, optional

        :raises RuntimeError: If an attempt is made to join the current thread (main thread), 
                               or if join() is called before start().
        """
        for thread in self.__threads:
            thread.join(timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the pipeline stage and wait for its threads to finish.

        :param timeout: The maximum time to wait for threads to finish. Defaults to None.
        :type timeout: float or None, optional

        :raises RuntimeError: If an attempt is made to join the current thread (main thread), 
                               or if join() is called before start().
        """
        self.stop()
        self.join(timeout=timeout)
