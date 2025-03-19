
from typing import Any, Iterable

from safethread.thread.utils.ThreadPipelineStage import ThreadPipelineStage


class ThreadPipeline:
    """
    A processing pipeline composed of interconnected `PipelineStage` instances.

    This class manages the sequential execution of pipeline stages, allowing data 
    to be passed through multiple stages of processing in a controlled manner.

    Example: input => Stage 1 => Stage 2 => ... => output    

    <img src="../../../img/utils/Pipeline.svg" alt="" width="100%">
    """

    def __init__(self, pipeline_stages: Iterable[ThreadPipelineStage]):
        """
        Initializes a pipeline with the given sequence of pipeline stages.

        :param pipeline_stages: A collection of `PipelineStage` instances that make up the pipeline.
        :type pipeline_stages: Iterable[PipelineStage]
        """
        super().__init__()

        self.__started = False
        self.__stages = tuple(pipeline_stages)
        self.__connect()

    def __connect(self):
        """
        Connects the pipeline stages sequentially.

        Each stage's output queue is connected to the next stage's input queue.
        """
        for i in range(len(self.__stages)-1):
            cur_stage = ThreadPipelineStage.is_instance(self.__stages[i])
            next_stage = ThreadPipelineStage.is_instance(self.__stages[i+1])
            cur_stage.connect_output(next_stage)

    def get(self, block: bool = True, timeout: float | None = None):
        """
        Retrieves processed data from the last stage of the pipeline.

        :param block: If True, waits for data to become available. Defaults to True.
        :type block: bool, optional
        :param timeout: Maximum wait time for data retrieval. Defaults to None.
        :type timeout: float | None, optional
        :return: The processed data retrieved from the last pipeline stage.
        :rtype: Any

        :raises EmptyException: If `block=True` and timeout is exceeded, or if `block=False` and no output is available in the output queue.
        :raises RuntimeError: If called on an Pipeline without PipelineStages (empty pipeline).
        """
        if len(self.__stages) == 0:
            raise RuntimeError(
                "Cannot get() output from an empty Pipeline (one that has no PipelineStages)")
        return self.__stages[-1].get(block=block, timeout=timeout)

    def put(self, input: Any, block: bool = True, timeout: float | None = None):
        """
        Sends data into the first stage of the pipeline for processing.

        :param input: The data to be processed by the pipeline.
        :type input: Any
        :param block: If True, waits until space is available in the input queue. Defaults to True.
        :type block: bool, optional
        :param timeout: Maximum wait time for insertion. Defaults to None.
        :type timeout: float | None, optional

        :raises FullException: If `block=True` and timeout is exceeded, or if `block=False` and there is no available space in the input queue.
        :raises StoppedException: If the pipeline has stopped.
        :raises RuntimeError: If called on an empty Pipeline (one that has no PipelineStages)
        """
        if len(self.__stages) == 0:
            raise RuntimeError(
                "Cannot put() input into an empty Pipeline (one that has no PipelineStages)")
        self.__stages[0].put(input, block=block, timeout=timeout)

    def has_started(self) -> bool:
        """
        Checks if the pipeline has started.

        :return: True if the pipeline has started, otherwise False.
        :rtype: bool
        """
        return self.__started

    def is_alive(self) -> bool:
        """
        Checks if all pipeline stages are alive.

        :return: True if all pipeline stages are alive, otherwise False.
        :rtype: bool
        """
        for stage in self.__stages:
            if not stage.is_alive():
                return False
        return True

    def is_terminated(self) -> bool:
        """
        Checks if the pipeline has terminated.

        :return: True if the pipeline HAS started and is NOT alive, otherwise False.
        :rtype: bool
        """
        return self.has_started() and not self.is_alive()

    def start(self):
        """
        Starts all pipeline stages.

        :raises RuntimeError: If start() is called more than once.
        """
        for stage in self.__stages:
            stage.start()
        self.__started = True

    def stop(self):
        """Stops all pipeline stages."""
        for stage in self.__stages:
            stage.stop()

    def join(self, timeout: float | None = None):
        """
        Waits for all pipeline stages to complete execution.

        :param timeout: The maximum time to wait for each pipeline stage to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: If join() is called before start().
        """
        for stage in self.__stages:
            stage.join(timeout=timeout)

    def stop_join(self, timeout: float | None = None):
        """
        Calls stop() and join() to stop the pipeline and wait for its stages to finish.

        :param timeout: The maximum time to wait for stages to finish. Defaults to None.
        :type timeout: float, optional

        :raises RuntimeError: If join() is called before start() or an attempt is made to join the current thread.
        """
        self.stop()
        self.join(timeout=timeout)
