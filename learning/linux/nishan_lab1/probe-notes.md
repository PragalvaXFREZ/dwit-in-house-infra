# Part 1: Shell Probe Notes

## 1. Predictions

Before running `probe.sh`, I predicted the following behaviour:

| Line | Feature | Bash prediction | Dash prediction |
|---|---|---|---|
| 1 | `echo -e` | Interprets `\t` as a tab | Prints `-e` literally and handles the escape differently |
| 2 | `$RANDOM` | Prints a random number | Variable is empty |
| 3 | Brace expansion | Prints `1 2 3` | Prints `{1..3}` literally |
| 4 | Single brackets `[ ]` | Works | Works |
| 5 | Double brackets `[[ ]]` | Works | Not supported |
| 6 | `source` | Works | Not supported |
| 7 | Dot command `.` | Works | Works |
| 8 | Arrays | Works | Not supported |

## 2. Actual Bash Output

```text
1. a    b
2. random: [random number]
3. 1 2 3
4. single bracket works
5. double bracket works
6. source works
7. dot works
8. second number: 20
```

## 3. Actual Dash Output

Dash successfully handles the POSIX-compatible features but does not support several Bash-specific features.

The script stops when it reaches the `[[ ]]` expression because Dash does not support Bash's double-bracket conditional syntax.

Other observed differences include:
- `$RANDOM` is not available in Dash.
- Brace expansion is not supported.
- `source` is not supported; the POSIX alternative is `.`.
- Bash arrays are not supported.

## 4. Three Important Differences

### Difference 1: Bash-specific syntax

Bash supports `[[ ]]`, arrays, and brace expansion. Dash does not support these Bash-specific features because it focuses on POSIX shell compatibility.

### Difference 2: Loading another script

Bash supports both `source` and `.`. Dash supports only `.`. The dot command is the portable POSIX way to load another shell script into the current shell.

### Difference 3: Random numbers

Bash provides the `$RANDOM` variable, which generates a pseudo-random number. Dash does not provide this variable, so it expands to an empty value.

## 5. Which Shell Runs the Script?

When the script uses:

```bash
#!/bin/sh
```

Debian runs it using Dash because `/bin/sh` points to Dash.

When the script uses:

```bash
#!/bin/bash
```

It runs using Bash.

## 6. Why Use Dash?

Dash supports fewer features than Bash, but it is smaller and generally starts faster. This makes it useful for system scripts that need standard shell features and execute frequently during system startup.


