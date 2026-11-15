# Part 1.7: Timing Notes — Bash vs Dash

## 1. Experiment Goal

The purpose of this experiment is to compare Bash and Dash in two situations:

- Running a shell loop that counts from 0 to 200,000.
- Measuring the cost of starting each shell 300 times.

For the loop test, both shells should print `200000`. The real time is used to compare how long each command takes from start to finish.

## 2. Prediction


My prediction is Dash will finish the loop sooner than Bash because Dash is a smaller shell with fewer features. I expected it to be around twice as fast, rather than ten times as fast.



## 3. Loop Timing Results

The loop script was run using:

```bash
time bash loop.sh
time dash loop.sh
```

Both commands printed `200000`.

### Loop Timing Measurements

| Shell | Run 1 — Real Time | Run 2 — Real Time | Run 3 — Real Time |
|---|---:|---:|---:|
| Bash | 0.436 s | 0.438 s | 0.414 s|
| Dash | 0.188 s | 0.192 s | 0.196 s |

### Comparison of the Recorded Run

- Average Bash: 0.429 seconds
- Average Dash: 0.192 seconds

Dash was approximately **2.23 times faster** in this recorded run.

Calculation:
`0.0.429 ÷ 0.192 ≈ 2.23`

## 4. Shell Start-up Cost

The start-up test runs the selected shell 300 times. The following commands were used:

### Bash Start-up Test

```bash
time sh -c 'i=0; while [ $i -lt 300 ]; do bash -c true; i=$((i+1)); done'
```

### Dash Start-up Test

```bash
time sh -c 'i=0; while [ $i -lt 300 ]; do dash -c true; i=$((i+1)); done'
```

### Bash Start-up Measurements

| Run | Real Time |
|---|---:|
| 1 | 0.552 s |
| 2 | 0.539 s |
| 3 | 0.547 s |
| 4 | 0.517 s |
| 5 | 0.568 s |
| **Average** | **0.545 s** |

### Dash Start-up Measurements

| Run | Real Time |
|---|---:|
| 1 | 0.346 s |
| 2 | 0.427 s |
| 3 | 0.311 s |
| 4 | 0.308 s |
| 5 | 0.319 s |
| **Average** | **0.342 s** |

### Start-up Comparison

The average Bash start-up test took approximately 0.545 seconds, while the average Dash start-up test took approximately 0.342 seconds.

Dash was approximately **1.59 times faster** in this test.

Calculation:`0.545 ÷ 0.342 ≈ 1.59`

## 5. Was the Prediction Correct?

The recorded results support the suggested prediction that Dash is faster than Bash for these tests:

- In the loop test, Dash took 0.192 seconds, compared with Bash at 0.429 seconds.
- In the 300-startup test, Dash averaged 0.342 seconds, compared with Bash at 0.545 seconds.

The difference was not the same in both tests. Dash was about 2.23 times faster in the multiple loop run and about 1.59 times faster in the repeated start-up test.

## 6. Why Start-up Time Matters on Linux

A Linux machine can run many small shell scripts during boot and while performing system tasks. In that situation, the time required to start a shell can matter as much as the time required to execute the script itself.

If a shell starts more quickly, the system can save time when launching many short scripts. The start-up experiment shows that Dash was faster than Bash when each was started 300 times. This helps explain why a lightweight shell such as Dash can be useful for system scripts.

The result does not mean Bash is always worse. Bash provides additional features that some scripts need. The appropriate shell depends on whether a script needs Bash-specific functionality or can use portable POSIX shell syntax.

## 7. Conclusion

In my measurements, Dash was faster than Bash in both the loop test and the repeated start-up test.

The loop ruan multiple times and record showed Dash taking 0.192 seconds and Bash taking 0.429 seconds. In the start-up test, the five-run averages were 0.342 seconds for Dash and 0.545 seconds for Bash.

This experiment demonstrates that a smaller shell can have performance advantages, particularly when many short scripts are launched. 
