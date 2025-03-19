import unittest
import sys

# Adjust the import to your module structure
from safethread.process import SubprocessProcess


def on_finish_succ(result: SubprocessProcess.Finished):
    command = []
    if sys.platform == "win32":
        command = ["cmd", "/c", "echo Hello, World!"]
    else:
        command = ["echo", "Hello, World!"]

    assert tuple(result.args) == tuple(command)
    assert result.stderr.strip() == ""
    assert result.stdout.strip() == "Hello, World!"
    assert result.returncode == 0


def on_finish_failing(result: SubprocessProcess.Finished):
    command = ["non_existing_command"]

    assert tuple(result.args) == tuple(command)
    assert result.stderr != ""
    assert result.returncode != 0


def on_finish_stderr_output(result: SubprocessProcess.Finished):
    err_msg = "Error Message"
    command = ["python", "-c",
               f"import sys; sys.stderr.write('{err_msg}\\n')"]

    assert tuple(result.args) == tuple(command)
    assert result.stderr.strip() == err_msg
    assert result.returncode == 0


def on_finish_long_command(result: SubprocessProcess.Finished):
    command = ["python", "-c", "import time; time.sleep(0.1)"]

    assert tuple(result.args) == tuple(command)
    assert result.stdout == ""
    assert result.stderr.strip() == ""
    assert result.returncode == 0


def on_finish_process_safety(result: SubprocessProcess.Finished):
    if sys.platform == "win32":
        command = ["cmd", "/c", "echo {{string}}"]
    else:
        command = ["echo", "{{string}}"]

    assert result.stdout == "{{string}}"
    assert result.stderr.strip() == ""
    assert result.returncode == 0


class TestSubprocessProcess(unittest.TestCase):

    def test_successful_execution(self):
        """Test if a simple command executes successfully across platforms."""
        command = []
        if sys.platform == "win32":
            command = ["cmd", "/c", "echo Hello, World!"]
        else:
            command = ["echo", "Hello, World!"]
        sp = SubprocessProcess(command)

        sp.start()
        sp.join()

        self.assertTrue(tuple(sp.get_args()[0]) == tuple(command))

        self.assertTrue(sp.is_terminated())

    def test_successful_on_finish(self):
        """Test if a simple command executes successfully across platforms."""
        command = []
        if sys.platform == "win32":
            command = ["cmd", "/c", "echo Hello, World!"]
        else:
            command = ["echo", "Hello, World!"]

        sp = SubprocessProcess(
            command,
            on_finish=on_finish_succ
        )

        sp.start()
        sp.join()

    def test_failing_command(self):
        """Test if an invalid command raises an exception, handling platform differences."""
        command = ["non_existing_command"]

        sp = SubprocessProcess(
            command,
            on_finish=on_finish_failing,
        )
        sp.start()
        sp.join()

        self.assertTrue(sp.is_terminated())

    def test_stderr_output(self):
        """Test if stderr is correctly captured."""
        err_msg = "Error Message"

        command = [
            "python", "-c",
            f"import sys; sys.stderr.write('{err_msg}\\n')",
        ]

        sp = SubprocessProcess(
            command,
            on_finish=on_finish_stderr_output,
        )

        sp.start()
        sp.join()

        self.assertTrue(sp.is_terminated())

    def test_long_running_command(self):
        """Test handling of long-running processes in a cross-platform way."""
        command = [
            "python", "-c",
            "import time; time.sleep(0.1)"
        ]

        sp = SubprocessProcess(
            command,
            on_finish=on_finish_long_command,
        )
        sp.start()
        self.assertFalse(sp.is_terminated())  # Should still be running

        sp.join()
        self.assertTrue(sp.is_terminated())  # Should be terminated now

    def test_process_safety(self):
        """Test multiple Subprocess instances running in parallel."""
        command = []
        if sys.platform == "win32":
            command = ["cmd", "/c", "echo {{string}}"]
        else:
            command = ["echo", "{{string}}"]

        processes = [
            SubprocessProcess(
                command,
                on_finish=on_finish_process_safety,
            ) for i in range(3)
        ]
        for p in processes:
            p.start()

        for p in processes:
            p.join()
            self.assertTrue(p.is_terminated())


if __name__ == "__main__":
    unittest.main()
