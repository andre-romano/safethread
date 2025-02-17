
import subprocess
import threading

from typing import Any, Callable, Iterable


class Subprocess:

    class Finished:
        def __init__(self, args: list[str], returncode: int, stderr: str, stdout: str):
            self.returncode = returncode
            self.args = args
            self.stderr = stderr
            self.stdout = stdout

    def __init__(self,
                 command: Iterable[str] | str, daemon: bool = True, timeout: float | None = None,
                 env: dict | None = None, cwd: str | None = None, callback: Callable | None = None):
        """
        Initializes the thread-safe Subprocess object with the command to run.

        Args:
            command (Iterable[str] | str): The command to run as an iterable or a string.
            daemon (bool, optional): Whether the thread should be a daemon thread. Defaults to True.
            timeout (float, optional): Timeout of the subprocess. Defaults to no timeout (None).
            env (dict, optional): Environment to run the subprocess. Defaults to current ENV (None).
            cwd (str, optional): Working directory to run the subprocess. Defaults to current directory (None).
            callback (Callable, optional): Callback to execute after subprocess terminates. Expected format: ``lambda result: some_code_here``, where `result: Subprocess.Finished`. Defaults to None.
        """
        cmd: list[str] = []
        if isinstance(command, str):
            cmd = command.split()
        elif isinstance(command, Iterable):
            cmd = list(command)
        else:
            raise TypeError(
                "Command must be a string or an iterable of strings.")

        self._lock = threading.RLock()
        self._result: Subprocess.Finished | None = None
        self._thread = threading.Thread(
            target=self._run, args=[cmd, timeout, env, cwd, callback],
            daemon=daemon
        )

    def _run(self,
             command: list[str], timeout: float | None, env: dict | None = None,
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
        with self._lock:
            try:
                result = subprocess.run(
                    command,
                    capture_output=True, text=True,
                    timeout=timeout, env=env,
                    cwd=cwd
                )
                self._result = Subprocess.Finished(
                    args=command,
                    returncode=result.returncode,
                    stderr=result.stderr,
                    stdout=result.stdout
                )
            except Exception as e:
                self._result = Subprocess.Finished(
                    args=command,
                    returncode=-1,
                    stderr=str(e),
                    stdout=''
                )
            finally:
                if callback:
                    callback(self._result)

    def get_return_code(self) -> int:
        """
        Returns the return code of the subprocess.

        Raises:
            Exception: If the subprocess has not yet terminated.

        Returns:
            int: The return code of the subprocess.
        """
        with self._lock:
            if not self.is_terminated() or not self._result:
                raise Exception("Cannot acquire return code from subprocess")
            return self._result.returncode

    def get_stdout(self) -> str:
        """
        Returns the standard output of the subprocess.

        Raises:
            Exception: If the subprocess has not yet terminated.

        Returns:
            str: The standard output of the subprocess.
        """
        with self._lock:
            if not self.is_terminated() or not self._result:
                raise Exception("Cannot acquire stdout from subprocess")
            return self._result.stdout

    def get_stderr(self) -> str:
        """
        Returns the standard error output of the subprocess.

        Raises:
            Exception: If the subprocess has not yet terminated.

        Returns:
            str: The standard error output of the subprocess.
        """
        with self._lock:
            if not self.is_terminated() or not self._result:
                raise Exception("Cannot acquire stderr from subprocess")
            return self._result.stderr

    def is_terminated(self) -> bool:
        """
        Checks if the subprocess has terminated.

        Returns:
            bool: True if the subprocess has terminated, otherwise False.
        """
        return not self._thread.is_alive()

    def join(self, timeout: float | None = None):
        """
        Joins the subprocess thread, waiting for it to finish.

        Args:
            timeout (float, optional): The maximum time to wait for the thread to finish. Defaults to None.
        """
        self._thread.join(timeout)

    def start(self):
        """
        Starts the subprocess in a separate thread.
        """
        self._thread.start()
