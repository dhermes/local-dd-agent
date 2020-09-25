#!/bin/sh

cd /var/code
python -m flask run --port "${TRACE_PORT}" --host 0.0.0.0
