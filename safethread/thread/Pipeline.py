
import queue

from typing import Any, Callable, Iterable

from .ThreadBase import ThreadBase


class Pipeline(ThreadBase):
    """
    A pipeline that processes data through a callback function in a separate thread.

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

    def __init__(self, callback: Callable):
        """
        Initializes the pipeline with a callback function.

        Args:

            callback (Callable): The function to process data through the pipeline.

        Raises:

            ThreadBase.CallableException: If the callback argument is not callable.
        """
        super().__init__(
            callback=self.__run_pipeline,
            repeat=True
        )

        self.__callback: Callable = self.check_callable(callback)
        self.__input_queue = queue.Queue()
        self.__output_queue = queue.Queue()

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

    def stop(self):
        """
        Stops the pipeline thread (immediately)
        """
        super().stop()
        try:
            self.__input_queue.shutdown(immediate=True)
            self.__output_queue.shutdown(immediate=True)
        except:
            pass
