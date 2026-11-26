# probe.sh: bash vs dash

## Prediction table

| Line | bash prints | dash prints |
| --- | --- | --- |
| 1 | `1. a     b` | `1. a    b` |
| 2 | `2. random: (a random number)` | Error |
| 3 | `3. {1..3}` | `3. {1..3}` |
| 4 | `4. single bracket works` | `4. single bracket works` |
| 5 | `5. double bracket works` | `5. double bracket works` |
| 6 | `6. source works` | Error |
| 7 | `7. dot works` | `7. dot works` |
| 8 | `8. second number: 20` | `8. second number: 20` |

## Actual output: bash

```
sulav@vm01:~/build1$ bash probe.sh
1. a	b
2. random: 29063
3. 1 2 3
4. single bracket works
5. double bracket works
6. source works
7. dot works
8. second number: 20
```

## Actual output: dash

```
sulav@vm01:~/build1$ dash probe.sh
-e 1. a	b
2. random: 
3. {1..3}
4. single bracket works
probe.sh: 5: [[: not found
probe.sh: 6: source: not found
7. dot works
probe.sh: 8: Syntax error: "(" unexpected
```

## Surprising differences

1. Arrays aren't supported in dash, hence the `"(" unexpected` error.
2. `echo` doesn't work fully in dash. It doesn't recognize the `-e` flag and prints it as text.
3. The double bracket `[[ ]]` doesn't exist in dash.

## Why would anyone choose the shell that can do less?

Debian has two shells installed and uses the smaller one for system scripts. My guess: dash must be faster and use less memory and CPU than bigger shells like bash.
