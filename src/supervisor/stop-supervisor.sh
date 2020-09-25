#!/bin/bash

# H/T: https://gist.github.com/tomazzaman/63265dfab3a9a61781993212fa1057cb

printf "READY\n";

while read line; do
  echo "[supervisord-cleanup] Processing Event: $line" >&2;
  kill -SIGQUIT "${PPID}"
done < /dev/stdin
