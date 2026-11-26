import os
import shlex
import subprocess
import sys
from contextlib import ExitStack

last_status = 0


def parse_command(command):
    """Parse commands, pipes, and redirections."""

    lexer = shlex.shlex(command, posix=True, punctuation_chars="|<>")
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

        if token == "|":
            if not args:
                raise ValueError("Invalid pipe syntax")

            commands.append(
                {
                    "args": args,
                    "input": input_file,
                    "output": output_file,
                    "append": append,
                }
            )

            args = []
            input_file = None
            output_file = None
            append = False

        elif token in ("<", ">", ">>"):
            if i + 1 >= len(tokens):
                raise ValueError("Missing filename for redirection")

            filename = tokens[i + 1]

            if filename in ("|", "<", ">", ">>"):
                raise ValueError("Invalid redirection filename")

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
            args.append(token)

        i += 1

    if not args:
        if tokens:
            raise ValueError("Invalid command syntax")
        return []

    commands.append(
        {"args": args, "input": input_file, "output": output_file, "append": append}
    )

    return commands


def execute_pipeline(commands):
    """Execute commands connected through pipes."""

    processes = []
    previous_read = None
    open_fds = set()

    try:
        for index, command in enumerate(commands):
            args = command["args"]
            is_last = index == len(commands) - 1

            # Create a pipe for the next command.
            if not is_last:
                read_fd, write_fd = os.pipe()
                open_fds.update((read_fd, write_fd))
            else:
                read_fd = None
                write_fd = None

            stdin = previous_read
            stdout = write_fd

            # Manage input and output redirection safely.
            with ExitStack() as stack:
                if command["input"]:
                    stdin = stack.enter_context(open(command["input"], "r"))

                if command["output"]:
                    mode = "a" if command["append"] else "w"
                    stdout = stack.enter_context(open(command["output"], mode))

                # Start the child process.
                process = subprocess.Popen(args, stdin=stdin, stdout=stdout)

                processes.append(process)

            # Close the parent's copy of the previous pipe.
            if previous_read is not None:
                os.close(previous_read)
                open_fds.discard(previous_read)

            # Close the parent's copy of the pipe's write end.
            if write_fd is not None:
                os.close(write_fd)
                open_fds.discard(write_fd)

            # Keep the read end for the next command.
            previous_read = read_fd

        # Wait for all commands.
        status = 0

        for process in processes:
            status = process.wait()

        return status

    except KeyboardInterrupt:
        print()

        # Stop remaining child processes.
        for process in processes:
            if process.poll() is None:
                try:
                    process.terminate()
                except ProcessLookupError:
                    pass

        for process in processes:
            process.wait()

        return 130

    except FileNotFoundError as error:
        print(f"mysh: {error}", file=sys.stderr)
        return 127

    except PermissionError as error:
        print(f"mysh: {error}", file=sys.stderr)
        return 126

    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"mysh: {error}", file=sys.stderr)

        # Stop and reap already-started processes.
        for process in processes:
            if process.poll() is None:
                try:
                    process.terminate()
                except ProcessLookupError:
                    pass

        for process in processes:
            process.wait()

        return 1

    finally:
        # Close any file descriptors still owned by the parent.
        for fd in open_fds:
            try:
                os.close(fd)
            except OSError:
                pass


def execute(commands):
    """Handle built-in commands and external commands."""

    global last_status

    if not commands:
        return

    # Handle cd in the parent shell.
    if len(commands) == 1:
        args = commands[0]["args"]

        if args[0] == "cd":
            try:
                if len(args) > 2:
                    raise ValueError("cd: too many arguments")

                path = args[1] if len(args) == 2 else os.path.expanduser("~")

                if path == "-":
                    path = os.environ.get("OLDPWD", os.getcwd())

                old_directory = os.getcwd()
                os.chdir(os.path.expanduser(path))

                os.environ["OLDPWD"] = old_directory

                if len(args) == 2 and args[1] == "-":
                    print(os.getcwd())

                last_status = 0

            except (OSError, ValueError) as error:
                print(f"mysh: {error}", file=sys.stderr)
                last_status = 1

            return

        if args[0] == "exit":
            sys.exit(last_status)

    # cd and exit cannot change the parent shell from a pipeline.
    for command in commands:
        if command["args"][0] in ("cd", "exit"):
            print(
                f"mysh: {command['args'][0]}: "
                "built-in command cannot be used in a pipeline",
                file=sys.stderr,
            )
            last_status = 1
            return

    last_status = execute_pipeline(commands)


def main():
    global last_status

    while True:
        try:
            command = input(f"[{last_status}] mysh> ")

            if not command.strip():
                continue

            commands = parse_command(command)
            execute(commands)

        except KeyboardInterrupt:
            print()
            continue

        except EOFError:
            print()
            break

        except ValueError as error:
            print(f"mysh: {error}", file=sys.stderr)
            last_status = 2

        except (OSError, subprocess.SubprocessError) as error:
            print(f"mysh: {error}", file=sys.stderr)
            last_status = 1


if __name__ == "__main__":
    main()
