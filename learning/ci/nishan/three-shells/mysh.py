
import os
import signal

last_status = 0

# Keep the shell running when Ctrl+C is pressed.
signal.signal(signal.SIGINT, signal.SIG_IGN)


while True:
    try:
        command = input(f"[{last_status}] mysh> ")
    except EOFError:
        break

    if not command.strip():
        continue

    args = command.split()

    # Built-in exit command
    if args[0] == "exit":
        break

    # Built-in cd command
    if args[0] == "cd":
        try:
            path = args[1] if len(args) > 1 else os.path.expanduser("~")
            os.chdir(path)
            last_status = 0
        except OSError as e:
            print(f"mysh: cd: {e}")
            last_status = 1
        continue

    # Check for a pipe
    if "|" in args:
        index = args.index("|")
        left_args = args[:index]
        right_args = args[index + 1:]

        read_fd, write_fd = os.pipe()

        # First child: runs the left command
        pid1 = os.fork()

        if pid1 == 0:
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            try:
                os.dup2(write_fd, 1)
                os.close(read_fd)
                os.close(write_fd)

                os.execvp(left_args[0], left_args)

            except OSError as e:
                print(f"mysh: {e}", file=__import__("sys").stderr)
                os._exit(127)

        # Second child: runs the right command
        pid2 = os.fork()

        if pid2 == 0:
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            try:
                os.dup2(read_fd, 0)
                os.close(read_fd)
                os.close(write_fd)

                os.execvp(right_args[0], right_args)

            except OSError as e:
                print(f"mysh: {e}", file=__import__("sys").stderr)
                os._exit(127)

        # Parent closes pipe and waits
        os.close(read_fd)
        os.close(write_fd)

        os.waitpid(pid1, 0)
        _, status = os.waitpid(pid2, 0)

        exit_code = os.waitstatus_to_exitcode(status)
        last_status = 128 + (-exit_code) if exit_code < 0 else exit_code

    else:
        # Create a child process
        pid = os.fork()

        if pid == 0:
            # Allow the child command to receive Ctrl+C
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            try:
                # Input redirection (<)
                if "<" in args:
                    index = args.index("<")
                    filename = args[index + 1]

                    fd = os.open(filename, os.O_RDONLY)
                    os.dup2(fd, 0)
                    os.close(fd)

                    args = args[:index] + args[index + 2:]

                # Error redirection (2>)
                if "2>" in args:
                    index = args.index("2>")
                    filename = args[index + 1]

                    fd = os.open(
                        filename,
                        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                        0o644
                    )
                    os.dup2(fd, 2)
                    os.close(fd)

                    args = args[:index] + args[index + 2:]

                # Output redirection (>)
                if ">" in args:
                    index = args.index(">")
                    filename = args[index + 1]

                    fd = os.open(
                        filename,
                        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                        0o644
                    )
                    os.dup2(fd, 1)
                    os.close(fd)

                    args = args[:index] + args[index + 2:]

                # Execute the command
                os.execvp(args[0], args)

            except OSError as e:
                print(f"mysh: {e}", file=__import__("sys").stderr)
                os._exit(127)

        else:
            # Parent waits for the child process
            _, status = os.waitpid(pid, 0)

            exit_code = os.waitstatus_to_exitcode(status)
            last_status = 128 + (-exit_code) if exit_code < 0 else exit_code
