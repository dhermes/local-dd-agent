FROM python:3.8.5-slim-buster

ENV METRICS_PORT=8125
ENV TRACE_PORT=8126
EXPOSE "${METRICS_PORT}/udp"
EXPOSE "${TRACE_PORT}/tcp"
ENV UDS_PATH=/var/run/datadog/dsd.socket

# NOTE: ``PYTHONUNBUFFERED`` **must** be set when running in a detached
#       container.
ENV PYTHONUNBUFFERED=true
ENV FLASK_APP app
ENV FLASK_ENV development

RUN python -m pip install --upgrade pip

COPY requirements.txt /var/code/requirements.txt
RUN python -m pip install --requirement /var/code/requirements.txt

COPY docker/flask-entrypoint.sh \
     src/supervisor/stop-supervisor.sh \
     /usr/local/bin/
COPY src/supervisor/supervisord.conf /var/conf/
COPY src/python/app.py \
     src/python/counter.py \
     src/python/parse_datagram.py \
     src/python/pretty_json.py \
     src/python/udp_server.py \
     src/python/uds_server.py \
     /var/code/
ENTRYPOINT ["/usr/local/bin/supervisord", "--configuration", "/var/conf/supervisord.conf"]
