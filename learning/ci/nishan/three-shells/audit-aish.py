#this fixes Quoted Operators (echo ">")#

import os
import sys
import shlex
import signal
import subprocess

last_status = 0


def unquote(token):
    """Remove quotes from a token while preserving its contents."""
    try:
        return shlex.split(token)[0] if token else token
    except ValueError:
        raise ValueError("Invalid quoting")


def parse_command(command):
    """Parse commands, pipelines, and redirections."""

    lexer = shlex.shlex(
        command,
        posix=False,
        punctuation_chars="|<>"
    )
    lexer.whitespace_split = True
    lexer.commenters = ""

    tokens = list(lexer)

    commands = []
    args = []
    input_file = None
    output_file = None
    append = False

    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Identify operators only when they are unquoted.
        if token in ("|", "<", ">", ">>"):

            if token == "|":
                if not args:
                    raise ValueError("Invalid pipe syntax")

                commands.append({
                    "args": args,
                    "input": input_file,
                    "output": output_file,
                    "append": append
                })

                args = []
                input_file = None
                output_file = None
                append = False

            else:
                if i + 1 >= len(tokens):
                    raise ValueError("Missing filename for redirection")

                filename_token = tokens[i + 1]

                if filename_token in ("|", "<", ">", ">>"):
                    raise ValueError("Invalid redirection filename")

                filename = unquote(filename_token)

                if token == "<":
                    if input_file is not None:
                        raise ValueError("Multiple input redirections")

                    input_file = filename

                else:
                    if output_file is not None:
                        raise ValueError("Multiple output redirections")

                    output_file = filename
                    append = token == ">>"

                i += 1

        else:
            args.append(unquote(token))

        i += 1

    if not args:
        if tokens:
            raise ValueError("Invalid command syntax")
        return []

    commands.append({
        "args": args,
        "input": input_file,
        "output": output_file,
        "append": append
    })

    return commands


def execute_pipeline(commands):
    """Execute commands connected through multiple pipes."""

    processes = []
    previous_read = None

    try:
        for index, command in enumerate(commands):

            args = command["args"]
            is_last = index == len(commands) - 1

            read_fd = None
            write_fd = None
            input_handle = None
            output_handle = None

            try:
                # Create a pipe for the next command.
                if not is_last:
                    read_fd, write_fd = os.pipe()

                stdin = previous_read
                stdout = write_fd

                # Input redirection.
                if command["input"]:
                    input_handle = open(command["input"], "r")
                    stdin = input_handle

                # Output redirection.
                if command["output"]:
                    mode = "a" if command["append"] else "w"
                    output_handle = open(command["output"], mode)
                    stdout = output_handle

                # Start the process.
                process = subprocess.Popen(
                    args,
                    stdin=stdin,
                    stdout=stdout,
                    preexec_fn=lambda: signal.signal(
                        signal.SIGINT, signal.SIG_DFL
                    )
                )

                processes.append(process)

            finally:
                # Always close parent-side handles.
                if previous_read is not None:
                    os.close(previous_read)
                    previous_read = None

                if write_fd is not None:
                    os.close(write_fd)
                    write_fd = None

                if input_handle is not None:
                    input_handle.close()

                if output_handle is not None:
                    output_handle.close()

            # Keep the new pipe's read end for the next command.
            previous_read = read_fd
            read_fd = None

        # Wait for every process.
        statuses = []

        for process in processes:
            statuses.append(process.wait())

        # Return the last command's exit status.
        return statuses[-1] if statuses else 0

    except Exception as error:

        # Close descriptors still owned by the parent.
        for fd in (previous_read, read_fd, write_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass

        # Stop and reap already-started processes.
        for process in processes:
            if process.poll() is None:
                try:
                    process.terminate()
                except OSError:
                    pass

        for process in processes:
            try:
                process.wait()
            except OSError:
                pass

        print(f"mysh: {error}", file=sys.stderr)

        if isinstance(error, FileNotFoundError):
            return 127

        if isinstance(error, PermissionError):
            return 126

        return 1


def execute_command(commands):
    """Execute built-in commands or external pipelines."""

    global last_status

    if not commands:
        return

    # Handle built-in commands.
    if len(commands) == 1:
        command = commands[0]
        args = command["args"]

        if not args:
            return

        if args[0] == "cd":

            try:
                directory = args[1] if len(args) > 1 else os.path.expanduser("~")
                os.chdir(directory)
                last_status = 0

            except OSError as error:
                print(f"mysh: cd: {error}", file=sys.stderr)
                last_status = 1

            return

        if args[0] == "exit":
            status = int(args[1]) if len(args) > 1 else last_status
            sys.exit(status)

    last_status = execute_pipeline(commands)


def main():
    """Main shell loop."""

    global last_status

    # Ignore Ctrl+C in the shell itself.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    while True:
        try:
            command = input("mysh> ")

            if not command.strip():
                continue

            try:
                commands = parse_command(command)
                execute_command(commands)

            except ValueError as error:
                print(f"mysh: {error}", file=sys.stderr)
                last_status = 2

            except KeyboardInterrupt:
                print()
                last_status = 130

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            last_status = 130


if __name__ == "__main__":
    main()
