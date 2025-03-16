from safethread.process import SubprocessProcess


def main():
    # Create an instance of SubprocessProcess
    process = SubprocessProcess(command=["echo", "Hello, World!"])

    # Start the process
    process.start()

    # Wait for the process to complete
    process.join()

    # Check the exit code
    if process.get_exitcode() == 0:
        print("Process completed successfully")
    else:
        print(f"Process failed with exit code {process.get_exitcode()}")


if __name__ == "__main__":
    main()
