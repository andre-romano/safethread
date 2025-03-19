

import multiprocessing

from typing import MutableSequence

from safethread.AbstractSubprocess import AbstractSubprocess

from safethread.process.BaseProcess import BaseProcess


class SubprocessProcess(AbstractSubprocess, BaseProcess):
    """
    A process-safe class for running subprocess commands.

    This class inherits from AbstractSubprocess and BaseProcess to provide functionality to run a command in a subprocess, capture its output, and handle its completion through a callback.
    """

    def _create_command_list(self) -> MutableSequence:
        return multiprocessing.Manager().list()
