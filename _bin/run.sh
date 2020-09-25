#!/bin/bash

set -e

# On EXIT `kill` our process and all processes in our process group, in
# particular the `forward_to.py` process in the background.
trap "kill 0" EXIT

if ! [ -x "$(command -v python3)" ]; then
  echo "Error: python3 is not installed." >&2
  exit 1
fi

if ! [ -x "$(command -v docker)" ]; then
  echo "Error: docker is not installed." >&2
  exit 1
fi

export DATADOG_HOSTNAME=localhost
export DATADOG_PORT=8125
if [ -z "${DATADOG_ADDRESS}" ]; then
  DATADOG_ADDRESS="$(dirname "${0}")/../var-run-datadog/dsd.socket"
  # macOS workaround for `readlink`; see https://stackoverflow.com/q/3572030/1068170
  DATADOG_ADDRESS=$(python -c "import os; print(os.path.realpath('${DATADOG_ADDRESS}'))")
  export DATADOG_ADDRESS
else
  export DATADOG_ADDRESS="${DATADOG_ADDRESS}"
fi

set -x
# NOTE: This is very imperfect. Since it gets backgrounded it won't stop the
#       parent (`run.sh`) process if this fails. Also, we'd really prefer to
#       **restart** `forward_to.py` if it flakes / falls over but the Docker
#       container continues to run.
python3 src/python/forward_to.py &

docker run \
  --name local-dd-agent \
  --rm \
  --interactive --tty \
  --publish 8125:8125/udp \
  --publish 8126:8126/tcp \
  dhermes/local-dd-agent:latest
