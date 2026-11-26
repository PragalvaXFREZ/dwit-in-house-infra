# Battery: one set of tests, four shells

| # | Type this | A correct shell does this | bash | dash | mysh | aish |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `echo hello` | prints hello | pass | pass | pass | pass |
| 2 | `false` | exit status 1 | pass | pass | pass | pass (status not shown) |
| 3 | `nosuchcmd` | error message, status 127, shell still alive | pass | pass | pass | pass (status not shown) |
| 4 | `cd /tmp` then `pwd` | prints /tmp | pass | pass | pass | pass |
| 5 | `cd /nosuchdir` | error message, shell still alive, same folder as before | pass | pass | pass | pass |
| 6 | `echo one > out.txt` then `cat out.txt` | prints one | pass | pass | pass | pass |
| 7 | `wc -c < out.txt` | prints 4 | pass | pass | pass | pass |
| 8 | `echo a b c \| wc -w` | prints 3 | pass | pass | pass | pass |
| 9 | `printf "b\na\nb\n" \| sort \| uniq -c` | one a, two b | pass | pass | pass | pass |
| 10 | `yes \| head -n 1` | prints y once and returns at once | pass | pass | pass | fail |
| 11 | `sleep 100`, then Ctrl-C | back at the prompt, shell still alive | pass | pass | pass | pass |
| 12 | leak check | the number does not grow | pass (4 → 4) | pass (3 → 3) | pass (3 → 3) | pass (3 → 3) |

## Outputs

```
sulav@vm01:~/build1$ bash < tests.txt
hello
status: 1
bash: line 4: nosuchcmd: command not found
status: 127
/tmp
bash: line 8: cd: /nosuchdir: No such file or directory
status: 1
/tmp
one
4
3
      1 a
      2 b
y
```

```
sulav@vm01:~/build1$ dash < tests.txt
hello
status: 1
dash: 4: nosuchcmd: not found
status: 127
/tmp
dash: 8: cd: can't cd to /nosuchdir
status: 2
/tmp
one
4
3
      1 a
      2 b
y
```

```
sulav@vm01:~/build1$ python3 mysh.py < tests.txt
[0] mysh> hello
[0] mysh> [1] mysh> status: $?
[0] mysh> nosuchcmd: command not found
[127] mysh> status: $?
[0] mysh> [0] mysh> /tmp
[0] mysh> cd: /nosuchdir: no such directory
[1] mysh> status: $?
[0] mysh> /tmp
[0] mysh> [0] mysh> one
[0] mysh> 4
[0] mysh> 3
[0] mysh>       1 a
      2 b
[0] mysh> y
[0] mysh>
```

## Leak check (mysh)

Session 1 ran `echo a | cat | cat` more than 20 times inside mysh. Session 2 counted the open file descriptors before and after:

```
sulav@vm01:~$ ls /proc/5840/fd | wc -l
3
sulav@vm01:~$ ls /proc/5840/fd | wc -l
3
```
