# Part 3–4: Shell Battery Results

This document records the results for Bash, Dash, the hand-written `mysh.py`, and the AI-generated `aish.py`.

**Result labels:**
- **PASS** — Observed behaviour matched the expected behaviour.
- **FAIL** — Observed behaviour did not match the expected behaviour.


## 1. Test Results

| # | Test | Expected Behaviour | Bash | Dash | mysh | aish |
|---|---|---|---|---|---|---|
| 1 | `echo hello` | Prints `hello` | PASS | PASS | PASS | PASS |
| 2 | `false` | Exit status is 1 | PASS | PASS | PASS | PASS |
| 3 | `nosuchcmd` | Error message, status 127, shell remains alive | PASS | PASS | PASS | PASS |
| 4 | `cd /tmp` then `pwd` | Prints `/tmp` | PASS | PASS | PASS | PASS |
| 5 | `cd /nosuchdir` | Error; shell remains alive in the previous directory | PASS | PASS | PASS | PASS|
| 6 | `echo one > out.txt` then `cat out.txt` | Prints `one` | PASS | PASS | PASS | PASS |
| 7 | `wc -c < out.txt` | Prints `4` | PASS | PASS | PASS | PASS |
| 8 | `echo a b c \| wc -w` | Prints `3` | PASS | PASS | PASS | PASS |
| 9 | `printf "b\na\nb\n" \| sort \| uniq -c` | One `a`, two `b` | PASS | PASS | FAIL | PASS|
| 10 | `yes \| head -n 1` | Prints `y` once and returns promptly | PASS | PASS | PASS*| PASS|
| 11 | `sleep 100`, then Ctrl-C | Returns to prompt; shell remains alive | PASS | PASS | PASS | PASS |
| 12 | Repeated-pipeline file-descriptor leak check | File-descriptor count does not grow | PASS | PASS | PASS* | PASS |

---

### Notes on Failures and Unusual Results

- **Test 9 — mysh: FAIL**
  - `mysh.py` supports only one pipe.
  - When given three commands connected by two pipes, it splits at the first pipe and passes the remaining text as arguments to the second command.
  - The observed `sort` error was:

    ```text
    sort: extra operand 'uniq' not allowed with -c
    ```

  - `printf` also reported a broken pipe.

- **Test 10 — mysh: PASS***
  - It printed `y` and returned to the prompt.
  - However, `yes` also printed a broken-pipe warning when `head` exited.
  - The required output and prompt behaviour were achieved, so this was recorded as a pass with a note.

- **Test 12 — mysh: PASS***
  - The reported file-descriptor count stayed at `3` before and after the repeated-pipeline check.

- **Test 12 — aish.py: PASS**
  - The initial file-descriptor count was 3. After executing ```echo a | cat | cat ``` twenty times, the count remained 3. This indicates that the generated shell correctly closed the pipe descriptors during this test.
  


## 2. Test 12: File-Descriptor Leak Check Details

| Shell | Initial Count | Count After Repeated Pipelines | Result |
|---|---:|---:|---|
| Bash | 4 | 4 | PASS |
| Dash | 4 | 4 | PASS |
| mysh | 3 | 3 | PASS |
| aish | 3 | 3 | PASS |

(The count can vary between shell implementations because the number of descriptors already open when the shell starts may differ.The important comparison is whether the count for the same running process increases after repeated pipelines.)

## Test that fails aish.py : Quoted Operators (`echo ">"`)

### Which Test Failed?

**A command with a quoted operator.**

I typed:

```bash
echo ">"
```

A correct shell (Bash or Dash) prints `>`. However, `aish` prints:

```text
mysh: Missing filename for redirection
```

and sets the exit status to `2`.

### 1. What Happened?

The quotes around `">"` were supposed to make it plain text, but `aish` treated it as a real redirection operator.

It looked for a filename after it, found none, and refused to run `echo`.

The command `echo "|"` fails in the same way, displaying:

```text
Invalid pipe syntax
```

### 2. The Cause

`shlex` in POSIX mode removes the quotes while tokenizing. Therefore, by the time `parse_command` checks:

```python
token in ("<", ">", ">>")
```

the quoted `">"` looks identical to an unquoted `>`.

As a result, the shell cannot distinguish between a literal argument and an actual redirection operator.

### 3. The Smallest Fix

Keep the quotes during tokenization so quoted operators can be distinguished from actual shell operators. Then strip the quotes only when the token is used as an argument or filename.

**In `parse_command`, keep quotes while classifying tokens:**

```python
lexer = shlex.shlex(command, posix=False, punctuation_chars="|<>")
```

**Add the following helper function:**

```python
def unquote(tok):
    return shlex.split(tok)[0] if tok and tok[0] in "'\"" else tok
```

**When adding tokens to arguments:**

```python
args.append(unquote(token))
```

**When reading a redirection filename:**

```python
filename = unquote(tokens[i + 1])
```

### 4. How the Fix Works

With this change, `">"` stays as the three characters `">"` (including the quotes) during token comparisons.

Therefore, it is no longer equal to `>`, so the shell treats it as an ordinary argument instead of a redirection operator.

After calling `unquote()`, the quotes are removed, and `echo` receives the literal character:

```text
>
```





**Conclusion:** The failure occurred because the shell removed quotation marks before identifying operators. Preserving quotes during tokenization allows `aish` to distinguish quoted operators from actual shell syntax and correctly execute these commands.





