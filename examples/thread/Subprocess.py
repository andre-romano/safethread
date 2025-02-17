
from safethread.thread import Subprocess

# USAGE EXAMPLE
if __name__ == "__main__":
    command = ["echo", "Hello, World!"]
    subprocess_obj = Subprocess(command)

    subprocess_obj.start()
    subprocess_obj.join()

    if subprocess_obj.is_terminated():
        print("Return code:", subprocess_obj.get_return_code())
        print("Standard output:", subprocess_obj.get_stdout())
        print("Standard error:", subprocess_obj.get_stderr())
