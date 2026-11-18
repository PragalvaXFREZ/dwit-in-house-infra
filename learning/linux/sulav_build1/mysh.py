import os
import shlex
import signal
import sys


def parse_redirects(args):
    # split "echo one > out.txt" into the command and the file names
    cmd, infile, outfile = [], None, None
    i = 0
    while i < len(args):
        if args[i] in (">", "<"):
            if i + 1 >= len(args):
                raise ValueError(f"syntax error: nothing after {args[i]}")
            if args[i] == ">":
                outfile = args[i + 1]
            else:
                infile = args[i + 1]
            i += 2
        else:
            cmd.append(args[i])
            i += 1
    return cmd, infile, outfile


def split_pipes(args):
    # split "ls -l | grep py | wc -l" into [["ls","-l"], ["grep","py"], ["wc","-l"]]
    parts = [[]]
    for word in args:
        if word == "|":
            parts.append([])
        else:
            parts[-1].append(word)
    if any(not part for part in parts):
        raise ValueError("syntax error near |")
    return parts


def run_child(cmd, infile, outfile):
    # runs in the child: point input/output at the files, then become the program
    # give the program normal signal behaviour (Ctrl-C kills it, broken pipe kills it)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        if infile:
            fd = os.open(infile, os.O_RDONLY)
            os.dup2(fd, 0)
            os.close(fd)
        if outfile:
            fd = os.open(outfile, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            os.dup2(fd, 1)
            os.close(fd)
    except OSError as e:
        print(f"{e.filename}: {e.strerror}", file=sys.stderr)
        os._exit(1)

    try:
        os.execvp(cmd[0], cmd)
    except FileNotFoundError:
        print(f"{cmd[0]}: command not found", file=sys.stderr)
        os._exit(127)
    except PermissionError:
        print(f"{cmd[0]}: permission denied", file=sys.stderr)
        os._exit(126)


last_status = 0

while True:
    # read a line; Ctrl+D quits
    try:
        line = input(f"[{last_status}] mysh> ")
    except EOFError:
        print()
        break
    except KeyboardInterrupt:
        # Ctrl-C at the prompt: just start a fresh line
        print()
        last_status = 130
        continue

    # split into words, understanding quotes like a real shell
    try:
        args = shlex.split(line)
    except ValueError as e:
        print(f"syntax error: {e}", file=sys.stderr)
        last_status = 2
        continue
    if not args:
        continue

    # builtins: run inside the shell itself, no fork
    if args[0] == "cd":
        path = args[1] if len(args) > 1 else os.path.expanduser("~")
        try:
            os.chdir(path)
            last_status = 0
        except FileNotFoundError:
            print(f"cd: {path}: no such directory", file=sys.stderr)
            last_status = 1
        except NotADirectoryError:
            print(f"cd: {path}: not a directory", file=sys.stderr)
            last_status = 1
        except PermissionError:
            print(f"cd: {path}: permission denied", file=sys.stderr)
            last_status = 1
        continue

    if args[0] == "exit":
        code = int(args[1]) if len(args) > 1 else last_status
        sys.exit(code)

    # split at | and take out < and > for each command
    try:
        commands = [parse_redirects(part) for part in split_pipes(args)]
    except ValueError as e:
        print(e, file=sys.stderr)
        last_status = 2
        continue
    if any(not cmd for cmd, _, _ in commands):
        print("syntax error: missing command", file=sys.stderr)
        last_status = 2
        continue

    # while the children run, the shell ignores Ctrl-C (they still get it)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # one pipe between each pair of commands: 3 commands need 2 pipes
    pipes = [os.pipe() for _ in range(len(commands) - 1)]

    pids = []
    for i, (cmd, infile, outfile) in enumerate(commands):
        pid = os.fork()
        if pid == 0:
            # child: read from the pipe before me, write into the pipe after me
            if i > 0:
                os.dup2(pipes[i - 1][0], 0)
            if i < len(pipes):
                os.dup2(pipes[i][1], 1)
            # close every pipe end, or the reader never sees "the end"
            for r, w in pipes:
                os.close(r)
                os.close(w)
            run_child(cmd, infile, outfile)
        pids.append(pid)

    # the shell uses no pipe ends, so it closes them all too
    for r, w in pipes:
        os.close(r)
        os.close(w)

    # wait for every child; the prompt shows the last command's status
    for pid in pids:
        _, status = os.waitpid(pid, 0)
        code = os.waitstatus_to_exitcode(status)
        # killed by a signal shows as 128 + signal number, like bash (Ctrl-C = 130)
        last_status = 128 - code if code < 0 else code

    if last_status == 130:
        print()

    # back at the prompt, Ctrl-C works normally again
    signal.signal(signal.SIGINT, signal.default_int_handler)

sys.exit(last_status)
