# Timing: bash vs dash (1.7)

## loop.sh

```sh
i=0
while [ $i -lt 200000 ]; do
  i=$((i+1))
done
echo $i
```

## Prediction

I predicted that dash finishes faster than bash by about 2 times.

## Results

```
sulav@vm01:~/build1$ time bash loop.sh
200000

real	0m1.425s
user	0m1.425s
sys	0m0.000s

sulav@vm01:~/build1$ time dash loop.sh
200000

real	0m0.598s
user	0m0.594s
sys	0m0.004s
```

| Shell | real time |
| --- | --- |
| bash | 1.425 s |
| dash | 0.598 s |

## Explanation

As I predicted, dash finished more than 2 times faster than bash. That's probably the reason the system uses dash as its shell: it needs to run hundreds of scripts, and that can be done faster with dash than with bash.
