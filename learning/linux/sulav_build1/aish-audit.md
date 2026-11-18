# Audit of aish.py

## Test 10 failed

1. **Which test:** 10, `yes | head -n 1`
2. **What happened:** it printed `y`, then the extra error `yes: standard output: Broken pipe`. bash prints only `y`.
3. **Cause:** Python ignores SIGPIPE, and each child inherits that through exec, so `yes` isn't stopped when `head` closes the pipe. Its write fails and it complains instead.
4. **Smallest fix:** add `signal.signal(signal.SIGPIPE, signal.SIG_DFL)` in the child.

## Tests 2 and 3

Counted as pass, but aish never shows the exit status.
