# Building my own shell in Python

## What I built

For Build 1, I started by comparing two shells that are already on Debian: bash and dash. I wrote `probe.sh`, predicted what each shell would print, and then ran it. dash failed on arrays, on `[[ ]]`, on `source`, and it printed the `-e` from `echo -e` as text. Then I timed a loop of 200,000 steps. bash took 1.425 seconds and dash took 0.598 seconds, more than twice as fast. That explains why Debian uses the smaller shell for system scripts: it has to run hundreds of them.

After that I built my own shell, `mysh.py`, one milestone at a time. It prints a prompt, reads a line, forks a child, and the child turns into the program with `execvp` while the parent waits with `waitpid`. Then I added the exit status in the prompt, `cd` and `exit` as builtins, `>` and `<` redirection with `os.open` and `os.dup2`, pipes with `os.pipe`, and Ctrl-C handling with the `signal` module.

The most useful lesson was why `cd` can never be a separate program. Every program runs in a forked child. If `cd` were a program, it would change the child's directory, the child would exit, and the shell would still be in the same place. So `cd` has to run inside the shell itself.

## The bug that took me longest

The bug that took me longest was in `yes | head -n 1`. My shell printed `y`, but then also `yes: standard output: Broken pipe`. The pipe itself was working, so at first I didn't understand what was wrong.

The cause is Python. Python ignores the SIGPIPE signal when it starts, and every child my shell forks inherits that setting, even after it turns into `yes`. Normally, when `head` exits and closes the only read end of the pipe, the kernel stops `yes` with SIGPIPE. In my shell, `yes` ignored it, its next write failed, and it complained. The fix was one line in the child before `execvp`: `signal.signal(signal.SIGPIPE, signal.SIG_DFL)`.

## What the assistant got wrong

At the end I gave an AI assistant one prompt: write a Unix shell in Python with pipes, input and output redirection, cd, and Ctrl-C handling. I saved its answer as `aish.py` without changing anything and ran my battery of 12 tests against bash, dash, mysh and aish.

aish was good. It handled quotes, pipes, redirection and Ctrl-C. But it failed test 10 with exactly the same bug I had: `yes | head -n 1` printed `Broken pipe`, because it never reset SIGPIPE in the child. It also never shows the exit status. It reads the status from `waitpid` and then throws it away, so after `false` or `nosuchcmd` there is no way to see 1 or 127.

What I learned from this: the assistant wrote code that looks complete, but it missed the same detail a beginner misses. The only way I found it was by testing, not by reading the code.
