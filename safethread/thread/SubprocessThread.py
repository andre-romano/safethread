import subprocess

from typing import Any, Callable, Iterable

from .BaseThread import BaseThread


class SubprocessThread(BaseThread):

    class Finished:
        """Stores information about the finished subprocess"""

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
            self.returncode = returncode
            self.args = tuple(args)
            self.stderr = stderr
            self.stdout = stdout

    def __init__(self,
                 command: Iterable[str] | str,
                 daemon: bool = True,
                 repeat: bool = False,
                 on_finish: Callable[[Finished], Any] = lambda res: None,
                 timeout: float | None = None,
                 cwd: str | None = None,
                 env: dict | None = None,
                 ):
        """
        Initializes the thread-safe Subprocess object with the command to run.

        :param command: The command to run as an iterable or a string.
        :type command: Iterable[str] | str

        :param daemon: Whether the thread should be a daemon thread. Defaults to True.
        :type daemon: bool, optional

        :param repeat: Whether the thread should execute subprocess repeatedly (until .stop() is called). Defaults to False.
        :type repeat: bool, optional

        :param on_finish: Callback to execute after subprocess terminates. Has one argument `result: Subprocess.Finished`. Defaults to `lambda res: None`.
        :type on_finish: Callable, optional

        :param timeout: Timeout of the subprocess. Defaults to None (no timeout).
        :type timeout: float, optional

        :param cwd: Working directory to run the subprocess. Defaults to None (current directory).
        :type cwd: str, optional

        :param env: Environment to run the subprocess. Defaults to current ENV (None).
        :type env: dict, optional

        :raises TypeError: If `command` is not a string or an iterable of strings.
        """
        # check command
        cmd: list[str] = []
        if isinstance(command, str):
            cmd = command.split()
        elif isinstance(command, Iterable):
            cmd = list(command)
        else:
            raise TypeError(
                "Command must be a string or an iterable of strings.")

        super().__init__(
            callback=self.__run_subprocess,
            args=[cmd],
            daemon=daemon,
            repeat=repeat,
        )

        # initialize
        self.__on_finish = on_finish
        self.__timeout = timeout
        self.__cwd = cwd
        self.__env = env

        # state variables
        self.__result: SubprocessThread.Finished = SubprocessThread.Finished(
            args=(),  # no command run
            returncode=-1,  # no command run
            stderr="",
            stdout="",
        )

    def __run_subprocess(self, command: list[str]):
        """
        Runs the command in a subprocess and captures the output.
        """
        try:
            process = subprocess.run(
                command,
                timeout=self.__timeout,
                env=self.__env,
                cwd=self.__cwd,
                capture_output=True,
                text=True,
            )
            self.__result = SubprocessThread.Finished(
                args=command,
                returncode=process.returncode,
                stderr=process.stderr,
                stdout=process.stdout
            )
        except Exception as e:
            self.__result = SubprocessThread.Finished(
                args=command,
                returncode=255,
                stderr=str(e),
                stdout=''
            )
        finally:
            self.__on_finish(self.__result)

    def get_return_code(self) -> int:
        """
        Returns the return code of the subprocess.

        :return: The return code of the subprocess. Returns 0 if process ended gracefully, > 0 if an error occurred, and < 0 if subprocess has not been started.
        :rtype: int
        """
        return self.__result.returncode

    def get_stdout(self) -> str:
        """
        Returns the standard output of the subprocess.

        :return: The standard output of the subprocess.
        :rtype: str
        """
        return self.__result.stdout

    def get_stderr(self) -> str:
        """
        Returns the standard error output of the subprocess.

        :return: The standard error output of the subprocess.
        :rtype: str
        """
        return self.__result.stderr
