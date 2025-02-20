

from typing import Any, Iterable

from .PipelineStage import PipelineStage


class Pipeline:
    """
    A processing pipeline composed by interconnected `PipelineStage` instances.

    This class manages the sequential execution of pipeline stages, allowing data 
    to be passed through multiple stages of processing in a controlled manner.

    E.g., input => Stage 1 => Stage 2 => ... => output
    """

    def __init__(self, pipeline_stages: Iterable[PipelineStage]):
        """
        Initializes a pipeline with the given sequence of pipeline stages.

        Args:

            pipeline_stages (Iterable[PipelineStage]): A collection of `PipelineStage` instances 
                                                       that make up the pipeline.
        """
        self.__started = False
        self.__stages = tuple(pipeline_stages)
        self.__connect()

    def __connect(self):
        """
        Connects the pipeline stages sequentially.

        Each stage's output queue is connected to the next stage's input queue.
        """
        for i in range(len(self.__stages)-1):
            cur_stage = PipelineStage.is_instance(self.__stages[i])
            next_stage = PipelineStage.is_instance(self.__stages[i+1])
            cur_stage.connect_output(next_stage)

    def get(self, block: bool = True, timeout: float | None = None):
        """
        Retrieves processed data from the last stage of the pipeline.

        Args:

            block (bool, optional): If True, waits for data to become available. Defaults to True.

            timeout (float | None, optional): Maximum wait time for data retrieval. Defaults to None.

        Returns:

            Any: The processed data retrieved from the last pipeline stage.

        Raises:

            EmptyException: If `block=True` and timeout is exceeded, or if `block=False` 
                            and no output is available in the output queue.

            RuntimeError: If called on an empty pipeline.
        """
        if len(self.__stages) == 0:
            raise RuntimeError("Cannot get() output from an Empty Pipeline")
        return self.__stages[-1].get(block=block, timeout=timeout)

    def put(self, input: Any, block: bool = True, timeout: float | None = None):
        """
        Sends data into the first stage of the pipeline for processing.

        Args:

            input (Any): The data to be processed by the pipeline.

            block (bool, optional): If True, waits until space is available in the input queue. Defaults to True.

            timeout (float | None, optional): Maximum wait time for insertion. Defaults to None.

        Raises:

            FullException: If `block=True` and timeout is exceeded, or if `block=False` 
                           and there is no available space in the input queue.

            StoppedException: If the pipeline has stopped.

            RuntimeError: If called on an empty pipeline.
        """
        if len(self.__stages) == 0:
            raise RuntimeError("Cannot put() input into an Empty Pipeline")
        self.__stages[0].put(input, block=block, timeout=timeout)

    def has_started(self) -> bool:
        """
        Checks if the pipeline has started.

        Returns:

            bool: True if the pipeline has started, otherwise False.
        """
        return self.__started

    def is_alive(self) -> bool:
        """
        Checks if the all pipeline stages are alive.

        Returns:

            bool: True if entire pipeline stages are alive, otherwise False.
        """
        for stage in self.__stages:
            if not stage.is_alive():
                return False
        return True

    def is_terminated(self) -> bool:
        """
        Checks if the pipeline has terminated.

        Returns:

            bool: True if pipeline HAS started and is NOT alive, otherwise False.
        """
        return self.has_started() and not self.is_alive()

    def join(self, timeout: float | None = None):
        """
        Waits for all pipeline stages to complete execution.

        Args:

            timeout (float, optional): The maximum time to wait for each pipeline stage to finish. Defaults to None.

        Raises:

            RuntimeError: if the join() is called before start()
        """
        for stage in self.__stages:
            stage.join(timeout=timeout)

    def start(self):
        """
        Starts all pipeline stages.        

        Raises:

            RuntimeError: if start() is called more than once.
        """
        for stage in self.__stages:
            stage.start()
        self.__started = True

    def stop(self):
        """Stops all pipeline stages"""
        for stage in self.__stages:
            stage.stop()
