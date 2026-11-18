#!/bin/bash
echo -e "1. a\tb"
echo "2. random: $RANDOM"
echo 3. {1..3}
[ 1 = 1 ] && echo "4. single bracket works"
[[ 1 == 1 ]] && echo "5. double bracket works"
source ./helper.sh && echo "6. source works"
. ./helper.sh && echo "7. dot works"
nums=(10 20 30)
echo "8. second number: ${nums[1]}"
