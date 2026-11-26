#!/usr/bin/env python3
import os
import shlex
import signal
import sys
from dataclasses import dataclass, field

try:
    import readline  # Enables arrow-key navigation and command history in input()
except ImportError:
    pass


@dataclass
class Command:
    args: list[str] = field(default_factory=list)
    stdin_file: str | None = None
    stdout_file: str | None = None
    append: bool = False


def parse_pipeline(line: str) -> list[Command]:
    """Tokenize a command line and split it into pipeline stages with redirections."""
    lexer = shlex.shlex(line, posix=True, punctuation_chars="|<>")
    lexer.whitespace_split = True
    tokens = list(lexer)

    if not tokens:
        return []

    commands: list[Command] = []
    current = Command()
    i = 0

    while i < len(tokens):
        tok = tokens[i]
        if tok == "|":
            if not current.args:
                raise ValueError("Syntax error near unexpected token '|'")
            commands.append(current)
            current = Command()
            i += 1
        elif tok == "<":
            if i + 1 >= len(tokens) or tokens[i + 1] in ("|", "<", ">", ">>"):
                raise ValueError("Syntax error: expected filename after '<'")
            current.stdin_file = tokens[i + 1]
            i += 2
        elif tok in (">", ">>"):
            if i + 1 >= len(tokens) or tokens[i + 1] in ("|", "<", ">", ">>"):
                raise ValueError(f"Syntax error: expected filename after '{tok}'")
            current.stdout_file = tokens[i + 1]
            current.append = tok == ">>"
            i += 2
        else:
            current.args.append(tok)
            i += 1

    if not current.args:
        raise ValueError("Syntax error: incomplete pipeline")

    commands.append(current)
    return commands


def run_builtin(cmd: Command) -> bool:
    """Execute built-in commands in the parent shell process. Returns True if handled."""
    name = cmd.args[0]

    if name == "exit":
        code = 0
        if len(cmd.args) > 1:
            try:
                code = int(cmd.args[1])
            except ValueError:
                print(f"exit: {cmd.args[1]}: numeric argument required", file=sys.stderr)
                code = 2
        sys.exit(code)

    if name == "cd":
        if len(cmd.args) > 2:
            print("cd: too many arguments", file=sys.stderr)
            return True

        target = cmd.args[1] if len(cmd.args) == 2 else "~"
        if target == "-":
            target = os.environ.get("OLDPWD", "")
            if not target:
                print("cd: OLDPWD not set", file=sys.stderr)
                return True
            print(target)
        else:
            target = os.path.expanduser(target)

        try:
            prev_dir = os.getcwd()
            os.chdir(target)
            os.environ["OLDPWD"] = prev_dir
            os.environ["PWD"] = os.getcwd()
        except OSError as e:
            print(f"cd: {e.strerror}: {target}", file=sys.stderr)
        return True

    return False


def execute_pipeline(commands: list[Command]) -> None:
    """Fork and wire up pipes and file redirections for a list of commands."""
    if len(commands) == 1 and commands[0].args[0] in ("cd", "exit"):
        run_builtin(commands[0])
        return

    num_cmds = len(commands)
    pipes = [os.pipe() for _ in range(num_cmds - 1)]
    pids: list[int] = []

    # Ignore SIGINT in the parent shell while foreground children execute
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    try:
        for i, cmd in enumerate(commands):
            pid = os.fork()
            if pid == 0:
                # Restore default Ctrl-C termination behavior inside child processes
                signal.signal(signal.SIGINT, signal.SIG_DFL)

                try:
                    # Connect stdin to previous pipe's read end
                    if i > 0:
                        os.dup2(pipes[i - 1][0], 0)

                    # Connect stdout to current pipe's write end
                    if i < num_cmds - 1:
                        os.dup2(pipes[i][1], 1)

                    # Close all inherited pipe descriptors in the child
                    for r_fd, w_fd in pipes:
                        os.close(r_fd)
                        os.close(w_fd)

                    # Apply file redirections (overriding pipe ends if both are present)
                    if cmd.stdin_file is not None:
                        fd = os.open(cmd.stdin_file, os.O_RDONLY)
                        os.dup2(fd, 0)
                        os.close(fd)

                    if cmd.stdout_file is not None:
                        flags = os.O_WRONLY | os.O_CREAT | (
                            os.O_APPEND if cmd.append else os.O_TRUNC
                        )
                        fd = os.open(cmd.stdout_file, flags, 0o644)
                        os.dup2(fd, 1)
                        os.close(fd)

                    os.execvp(cmd.args[0], cmd.args)
                except FileNotFoundError:
                    os.write(2, f"{cmd.args[0]}: command not found\n".encode())
                    os._exit(127)
                except OSError as e:
                    os.write(2, f"{cmd.args[0]}: {e.strerror}\n".encode())
                    os._exit(1)
            else:
                pids.append(pid)

        # Close all pipe descriptors in the parent so downstream readers receive EOF
        for r_fd, w_fd in pipes:
            os.close(r_fd)
            os.close(w_fd)

        interrupted = False
        for pid in pids:
            _, status = os.waitpid(pid, 0)
            if os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGINT:
                interrupted = True

        if interrupted:
            print()
    finally:
        # Restore KeyboardInterrupt behavior at the interactive prompt
        signal.signal(signal.SIGINT, signal.default_int_handler)


def main() -> None:
    signal.signal(signal.SIGINT, signal.default_int_handler)

    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~", 1)
            line = input(f"\033[1;32m{cwd}\033[0m $ ")
        except KeyboardInterrupt:
            # Ctrl-C at an empty or partially typed prompt prints a newline and resets
            print()
            continue
        except EOFError:
            # Ctrl-D exits cleanly
            print()
            break

        try:
            commands = parse_pipeline(line)
            if commands:
                execute_pipeline(commands)
        except ValueError as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
