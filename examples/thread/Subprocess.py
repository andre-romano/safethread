
import sys
from safethread.thread import Subprocess

# USAGE EXAMPLE
if __name__ == "__main__":

    def on_finish(result: Subprocess.Finished):
        print("----------------------")
        print("     On_Finish()      ")
        print("----------------------")
        print(f"Args: {result.args}")
        print(f"Return Code: {result.returncode}")
        print(f"StdOut: {result.stdout}")
        print(f"StdErr: {result.stderr}")

    if sys.platform == "win32":
        command = ["cmd", "/c", "echo HELLO THERE"]
    else:
        command = ["echo", "HELLO THERE"]

    subprocess_obj = Subprocess(
        command=command,
        on_finish=on_finish,
    )

    subprocess_obj.start()
    subprocess_obj.join()

    if subprocess_obj.is_terminated():
        print("----------------------")
        print("Subprocess terminated!")
        print("----------------------")
        print("Return code:", subprocess_obj.get_return_code())
        print("Standard output:", subprocess_obj.get_stdout())
        print("Standard error:", subprocess_obj.get_stderr())
