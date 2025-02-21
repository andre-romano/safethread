import subprocess

from typing import Any, Callable, Iterable

from .ThreadBase import ThreadBase


class Subprocess(ThreadBase):

    class NotTerminatedException(Exception):
        """Raised when trying to get return data about an unfinished subprocess"""

    class Finished:
        """Stores information about the finished subprocess"""

        def __init__(self, args: list[str], returncode: int, stderr: str, stdout: str):
            """Creates a Finished structure for a recently finished subprocess

            :param args: Command arguments of subprocess
            :type args: list[str]
            :param returncode: Return code of subprocess
            :type returncode: int
            :param stderr: STDERR output of subprocess
            :type stderr: str
            :param stdout: STDOUT output of subprocess
            :type stdout: str
            """
            self.returncode = returncode
            self.args = args
            self.stderr = stderr
            self.stdout = stdout

    def __init__(self,
                 command: Iterable[str] | str, daemon: bool = True, timeout: float | None = None,
                 env: dict | None = None, cwd: str | None = None, callback: Callable | None = None,
                 repeat: bool = False):
        """
        Initializes the thread-safe Subprocess object with the command to run.

        :param command: The command to run as an iterable or a string.
        :type command: Iterable[str] | str
        :param daemon: Whether the thread should be a daemon thread. Defaults to True.
        :type daemon: bool, optional
        :param timeout: Timeout of the subprocess. Defaults to no timeout (None).
        :type timeout: float, optional
        :param env: Environment to run the subprocess. Defaults to current ENV (None).
        :type env: dict, optional
        :param cwd: Working directory to run the subprocess. Defaults to current directory (None).
        :type cwd: str, optional
        :param callback: Callback to execute after subprocess terminates. Expected format: ``lambda result: some_code_here``, where `result: Subprocess.Finished`. Defaults to None.
        :type callback: Callable, optional
        :param repeat: Whether the thread should execute subprocess repeatedly (until .stop() is called). Defaults to False.
        :type repeat: bool, optional

        :raises TypeError: If `command` is not a string or an iterable of strings.
        """
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
            args=[cmd, timeout, env, cwd, callback],
            daemon=daemon,
            repeat=repeat
        )
        self.__result: Subprocess.Finished | None = None
        self.__lock = self.get_lock()

    def __run_subprocess(self, command: list[str], timeout: float | None, env: dict | None = None,
                         cwd: str | None = None, callback: Callable | None = None):
        """
        Runs the command in a subprocess and captures the output.

        :param command: The command to execute.
        :type command: list[str]
        :param timeout: Timeout of the command.
        :type timeout: float, optional
        :param env: Environment for the command.
        :type env: dict, optional
        :param cwd: Current working directory for the command.
        :type cwd: str, optional
        :param callback: Callback to execute after subprocess terminates.
        :type callback: Callable, optional
        """
        with self.__lock:
            try:
                result = subprocess.run(
                    command,
                    capture_output=True, text=True,
                    timeout=timeout, env=env,
                    cwd=cwd
                )
                self.__result = Subprocess.Finished(
                    args=command,
                    returncode=result.returncode,
                    stderr=result.stderr,
                    stdout=result.stdout
                )
            except Exception as e:
                self.__result = Subprocess.Finished(
                    args=command,
                    returncode=-1,
                    stderr=str(e),
                    stdout=''
                )
            finally:
                if callback:
                    callback(self.__result)

    def get_return_code(self) -> int:
        """
        Returns the return code of the subprocess.

        :raises NotTerminatedException: If the subprocess has not yet terminated.

        :return: The return code of the subprocess.
        :rtype: int
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Process not terminated. Cannot acquire return code from subprocess")
            return self.__result.returncode

    def get_stdout(self) -> str:
        """
        Returns the standard output of the subprocess.

        :raises NotTerminatedException: If the subprocess has not yet terminated.

        :return: The standard output of the subprocess.
        :rtype: str
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Process not terminated. Cannot acquire stdout from subprocess")
            return self.__result.stdout

    def get_stderr(self) -> str:
        """
        Returns the standard error output of the subprocess.

        :raises NotTerminatedException: If the subprocess has not yet terminated.

        :return: The standard error output of the subprocess.
        :rtype: str
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Process not terminated. Cannot acquire stderr from subprocess")
            return self.__result.stderr
