

from typing import MutableSequence

from safethread.AbstractSubprocess import AbstractSubprocess

from safethread.thread.BaseThread import BaseThread


class SubprocessThread(AbstractSubprocess, BaseThread):
    """
    A thread-safe class for running subprocess commands.

    This class inherits from AbstractSubprocess and BaseThread to provide functionality to run a command in a subprocess, capture its output, and handle its completion through a callback.
    """

    def _create_command_list(self) -> MutableSequence:
        return list()
