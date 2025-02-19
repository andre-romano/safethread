
import subprocess

from typing import Any, Callable, Iterable

from .ThreadBase import ThreadBase


class Subprocess(ThreadBase):

    class NotTerminatedException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    class Finished:
        def __init__(self, args: list[str], returncode: int, stderr: str, stdout: str):
            """Stores information about the finished subprocess"""
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

        Args:

            command (Iterable[str] | str): The command to run as an iterable or a string.

            daemon (bool, optional): Whether the thread should be a daemon thread. Defaults to True.

            timeout (float, optional): Timeout of the subprocess. Defaults to no timeout (None).

            env (dict, optional): Environment to run the subprocess. Defaults to current ENV (None).

            cwd (str, optional): Working directory to run the subprocess. Defaults to current directory (None).

            callback (Callable, optional): Callback to execute after subprocess terminates. Expected format: ``lambda result: some_code_here``, where `result: Subprocess.Finished`. Defaults to None.

            repeat (bool, optional): Whether the thread should execute subprocess repeatedly (until .stop() is called). Defaults to False.
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

        Args:

            command (list[str]): The command to execute.

            timeout (float, optional): Timeout of the command.

            env (float, optional): Environment for the command.

            cwd (str, optional): Current working directory for the command.

            callback (Callable, optional): Callback to execute after subprocess terminates.
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

        Raises:

            NotTerminatedException: If the subprocess has not yet terminated.

        Returns:

            int: The return code of the subprocess.
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Cannot acquire return code from subprocess")
            return self.__result.returncode

    def get_stdout(self) -> str:
        """
        Returns the standard output of the subprocess.

        Raises:

            NotTerminatedException: If the subprocess has not yet terminated.

        Returns:

            str: The standard output of the subprocess.
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Cannot acquire stdout from subprocess")
            return self.__result.stdout

    def get_stderr(self) -> str:
        """
        Returns the standard error output of the subprocess.

        Raises:

            Exception: If the subprocess has not yet terminated.

        Returns:

            str: The standard error output of the subprocess.
        """
        with self.__lock:
            if not self.is_terminated() or not self.__result:
                raise Subprocess.NotTerminatedException(
                    "Cannot acquire stderr from subprocess")
            return self.__result.stderr
