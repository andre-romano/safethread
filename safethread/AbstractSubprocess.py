import subprocess

from typing import Any, Callable, Iterable, MutableSequence, Self

from safethread.AbstractPicklable import AbstractPicklable
from safethread.AbstractParallel import AbstractParallel


def _run_subprocess(
        command: Iterable[str],
        on_finish: Callable,
        timeout: float | None,
        cwd: str | None,
        env: dict | None,
) -> bool:
    """
    Runs the command in a subprocess and captures the output.
    """
    cmd = list(command)
    result = AbstractSubprocess.Finished(
        [], returncode=254, stderr="", stdout="")
    # This automatically closes pipes when the block exits
    try:
        with subprocess.Popen(
            cmd, cwd=cwd, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ) as process:
            try:
                stdout, stderr = process.communicate(timeout=timeout)

                result = AbstractSubprocess.Finished(
                    args=cmd,
                    returncode=process.returncode,
                    stderr=stderr.strip(),
                    stdout=stdout.strip()
                )
            except Exception as e:
                process.kill()
                stdout, stderr = process.communicate()  # Read remaining output
                result = AbstractSubprocess.Finished(
                    args=cmd,
                    returncode=process.returncode if process.returncode != 0 else 255,
                    stderr=f"{e}: {stderr.strip()}",
                    stdout=stdout.strip()
                )
    except Exception as e:
        # Handle cases where subprocess creation fails or other errors occur
        result = AbstractSubprocess.Finished(
            args=cmd,
            returncode=255,
            stderr=f"{e}",
            stdout=""
        )
    on_finish(result)
    return True


def _dummy_on_finish(result: Any) -> Any:
    return


class AbstractSubprocess(AbstractParallel):
    """
    A safe class for running subprocess commands.

    This class inherits from AbstractParallel and provides functionality to run a command in a subprocess, capture its output, and handle its completion through a callback.
    """

    class Finished(AbstractPicklable):
        """
        Stores information about the finished subprocess.

        Attributes:
            args (tuple): Command arguments of the subprocess.
            returncode (int): Return code of the subprocess.
            stderr (str): STDERR output of the subprocess.
            stdout (str): STDOUT output of the subprocess.
        """

        def __init__(
                self,
                args: Iterable[str],
                returncode: int,
                stderr: str,
                stdout: str,
        ):
            """Creates a Finished structure for a recently finished subprocess

            :param args: Command arguments of subprocess
            :type args: Iterable[str]

            :param returncode: Return code of subprocess
            :type returncode: int

            :param stderr: STDERR output of subprocess
            :type stderr: str

            :param stdout: STDOUT output of subprocess
            :type stdout: str
            """
            super().__init__()

            self.args = tuple(args)
            self.returncode = returncode
            self.stderr = stderr
            self.stdout = stdout

        def __reduce__(self) -> tuple[type[Self], tuple]:
            return (self.__class__, (
                self.args,
                self.returncode,
                self.stderr,
                self.stdout,
            ))

    def __init__(self,
                 command: Iterable[str] | str,
                 daemon: bool = True,
                 repeat: bool = False,
                 on_finish: Callable[[Finished], Any] = _dummy_on_finish,
                 timeout: float | None = None,
                 cwd: str | None = None,
                 env: dict | None = None,
                 ):
        """
        Initializes the process-safe Subprocess object with the command to run.

        :param command: The command to run as an iterable or a string.
        :type command: Iterable[str] | str

        :param daemon: Whether the process should be a daemon process. Defaults to True.
        :type daemon: bool, optional

        :param repeat: Whether the process should execute subprocess repeatedly (until .stop() is called). Defaults to False.
        :type repeat: bool, optional

        :param on_finish: Callback to execute after subprocess terminates. Has one argument `result: Subprocess.Finished`. Defaults to `lambda res: None`.
        :type on_finish: Callable, optional

        :param timeout: Timeout of the subprocess. Defaults to None (no timeout).
        :type timeout: float, optional

        :param cwd: Working directory to run the subprocess. Defaults to None (current directory).
        :type cwd: str, optional

        :param env: Environment to run the subprocess. Defaults to current ENV (None).
        :type env: dict, optional

        :raises TypeError: If `command` is not a string or an iterable of strings, or if `callback` is not callable.
        """
        # exception handling
        e: Exception | None = None

        # check command
        cmd = self._create_command_list()
        if isinstance(command, str):
            cmd.extend(command.split())
        elif isinstance(command, Iterable):
            cmd.extend(list(command))
        else:
            e = TypeError(
                "Command must be a string or an iterable of strings.")

        # check on_finish
        if not callable(on_finish):
            e = TypeError("on_finish() is not callable.")

        # initialize
        self.__timeout = timeout
        self.__cwd = cwd
        self.__env = env

        # call super
        super().__init__(
            callback=_run_subprocess,
            args=[
                cmd,
                on_finish,
                self.__timeout,
                self.__cwd,
                self.__env,
            ],
            daemon=daemon,
            repeat=repeat,
        )

        # raise exception, if needed
        if e:
            raise e

    def _create_command_list(self) -> MutableSequence:
        """
        Creates a list of commands to be executed by the subprocess.

        This method should be overridden by subclasses to provide the specific
        commands needed for the subprocess.

        :return: A list of commands for the subprocess.
        :rtype: MutableSequence

        :raises NotImplementedError: If the method is not overridden by a subclass.        
        """
        raise NotImplementedError("Method NOT overloaded")
