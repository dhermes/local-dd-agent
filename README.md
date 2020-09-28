# `local-dd-agent`

> "Mock" Datadog Agent That Can Be Run Locally

## Motivation

During local development, developers often just turn off `datadog`. We just
trust that our application metrics and traces will work as expected when
deployed to environments where `dd-agent` is running.

This is especially challenging when things **go wrong**. For example, sometimes
a task will exit before flushing all metrics out to `dd-agent` and debugging
an application in Kubernetes is a much larger challenge than debugging it
on a development machine. Or sometimes a client library may have a latent
bug we don't discover until production.

## Usage

```
$ make  # or `make help`
Makefile for `local-dd-agent` project

Usage:
   make build    Build Docker container with `local-dd-agent`
   make run      Run Docker container with `local-dd-agent` in the foreground

```

To build

```
$ make build
docker build \
          --tag dhermes/local-dd-agent:latest \
          --file docker/datadog.Dockerfile \
          .
Sending build context to Docker daemon  27.14kB
Step 1/16 : FROM python:3.8.5-slim-buster
 ---> ec75d34adff9
...
Removing intermediate container 12c4359fa62e
 ---> ab9fe6ed4e8f
Successfully built ab9fe6ed4e8f
Successfully tagged dhermes/local-dd-agent:latest
```

To run

```
$ make run
+ docker run --name local-dd-agent --rm --interactive --tty --publish 8125:8125/udp --publish 8126:8126/tcp dhermes/local-dd-agent:latest
+ python3 src/python/forward_to.py
2020-09-25 03:17:03,249 INFO Set uid to user 0 succeeded
2020-09-25 03:17:03,250 INFO supervisord started with pid 1
2020-09-25 03:17:04,258 INFO spawned: 'processes' with pid 8
2020-09-25 03:17:04,261 INFO spawned: 'port-8125' with pid 9
2020-09-25 03:17:04,264 INFO spawned: 'port-8126' with pid 10
2020-09-25 03:17:04,266 INFO spawned: 'uds' with pid 11
READY
...
```

and the UDS path can be overriden on the host (it will default to
`$(pwd)/var-run-datadog/dsd.socket` if not supplied):

```
$ make run DATADOG_ADDRESS="${HOME}/Desktop/dsd.socket"
...
```

## Example `local-dd-agent` Logs

![local-dd-agent logs][1]

```
001-001-8126 | trace =
001-001-8126 | {
001-001-8126 |   "trace_id": 529874070487136501,
001-001-8126 |   "span_id": 529874070487136501,
001-001-8126 |   "start": 1600440805460069888,
001-001-8126 |   "duration": 9042725,
001-001-8126 |   "error": 0,
001-001-8126 |   "parent_id": 0,
001-001-8126 |   "name": "serverInit",
001-001-8126 |   "resource": "serverInit",
001-001-8126 |   "service": "dd-sanity-check",
001-001-8126 |   "meta": {
001-001-8126 |     "service": "dd-sanity-check",
001-001-8126 |     "env": "dev",
001-001-8126 |     "version": "",
001-001-8126 |     "language": "javascript"
001-001-8126 |   },
001-001-8126 |   "metrics": {
001-001-8126 |     "_sample_rate": 1.0,
001-001-8126 |     "_dd.agent_psr": 1.0,
001-001-8126 |     "_sampling_priority_v1": 1.0
001-001-8126 |   }
001-001-8126 | }
172.17.0.1 - - [18/Sep/2020 14:53:27] "PUT /v0.4/traces HTTP/1.1" 200 -
001-001-8125 | metric =
001-001-8125 | {
001-001-8125 |   "raw_binary": "ZGQtc2FuaXR5LWNoZWNrLnJlcXVlc3Q6MXxjfCNwYXRoOi8=",
001-001-8125 |   "raw": "dd-sanity-check.request:1|c|#path:/",
001-001-8125 |   "metric": {
001-001-8125 |     "name": "dd-sanity-check.request",
001-001-8125 |     "value": "1"
001-001-8125 |   },
001-001-8125 |   "type": "COUNT",
001-001-8125 |   "tags": [
001-001-8125 |     "path:/"
001-001-8125 |   ]
001-001-8125 | }
002-002-8125 | metric =
002-002-8125 | {
002-002-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX2NvZGUuYWxsOjF8Y3wjcm91dGU6KixtZXRob2Q6R0VULHJlc3BvbnNlX2NvZGU6MjAwLHNlcnZpY2U6ZGQtc2FuaXR5LWNoZWNr",
002-002-8125 |   "raw": "api.requests.response_code.all:1|c|#route:*,method:GET,response_code:200,service:dd-sanity-check",
002-002-8125 |   "metric": {
002-002-8125 |     "name": "api.requests.response_code.all",
002-002-8125 |     "value": "1"
002-002-8125 |   },
002-002-8125 |   "type": "COUNT",
002-002-8125 |   "tags": [
002-002-8125 |     "route:*",
002-002-8125 |     "method:GET",
002-002-8125 |     "response_code:200",
002-002-8125 |     "service:dd-sanity-check"
002-002-8125 |   ]
002-002-8125 | }
003-003-8125 | metric =
003-003-8125 | {
003-003-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX2NvZGUuMjAwOjF8Y3wjcm91dGU6KixtZXRob2Q6R0VULHJlc3BvbnNlX2NvZGU6MjAwLHNlcnZpY2U6ZGQtc2FuaXR5LWNoZWNr",
003-003-8125 |   "raw": "api.requests.response_code.200:1|c|#route:*,method:GET,response_code:200,service:dd-sanity-check",
003-003-8125 |   "metric": {
003-003-8125 |     "name": "api.requests.response_code.200",
003-003-8125 |     "value": "1"
003-003-8125 |   },
003-003-8125 |   "type": "COUNT",
003-003-8125 |   "tags": [
003-003-8125 |     "route:*",
003-003-8125 |     "method:GET",
003-003-8125 |     "response_code:200",
003-003-8125 |     "service:dd-sanity-check"
003-003-8125 |   ]
003-003-8125 | }
004-004-8125 | metric =
004-004-8125 | {
004-004-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX3RpbWU6N3xofCNyb3V0ZToqLG1ldGhvZDpHRVQscmVzcG9uc2VfY29kZToyMDAsc2VydmljZTpkZC1zYW5pdHktY2hlY2s=",
004-004-8125 |   "raw": "api.requests.response_time:7|h|#route:*,method:GET,response_code:200,service:dd-sanity-check",
004-004-8125 |   "metric": {
004-004-8125 |     "name": "api.requests.response_time",
004-004-8125 |     "value": "7"
004-004-8125 |   },
004-004-8125 |   "type": "HISTOGRAM",
004-004-8125 |   "tags": [
004-004-8125 |     "route:*",
004-004-8125 |     "method:GET",
004-004-8125 |     "response_code:200",
004-004-8125 |     "service:dd-sanity-check"
004-004-8125 |   ]
004-004-8125 | }
002-002-8126 | trace =
002-002-8126 | {
002-002-8126 |   "trace_id": 6094184664711840243,
002-002-8126 |   "span_id": 8835503473541868521,
002-002-8126 |   "start": 1600440824028314112,
002-002-8126 |   "duration": 443359,
002-002-8126 |   "error": 0,
002-002-8126 |   "parent_id": 6094184664711840243,
002-002-8126 |   "name": "express.middleware",
002-002-8126 |   "resource": "query",
002-002-8126 |   "service": "dd-sanity-check",
002-002-8126 |   "meta": {
002-002-8126 |     "service": "dd-sanity-check",
002-002-8126 |     "env": "dev",
002-002-8126 |     "version": "",
002-002-8126 |     "language": "javascript"
002-002-8126 |   },
002-002-8126 |   "metrics": {
002-002-8126 |     "_sample_rate": 1.0,
002-002-8126 |     "_sampling_priority_v1": 1.0
002-002-8126 |   }
002-002-8126 | }
003-002-8126 | trace =
003-002-8126 | {
003-002-8126 |   "trace_id": 6094184664711840243,
003-002-8126 |   "span_id": 5727076931858754836,
003-002-8126 |   "start": 1600440824028803584,
003-002-8126 |   "duration": 180176,
003-002-8126 |   "error": 0,
003-002-8126 |   "parent_id": 6094184664711840243,
003-002-8126 |   "name": "express.middleware",
003-002-8126 |   "resource": "expressInit",
003-002-8126 |   "service": "dd-sanity-check",
003-002-8126 |   "meta": {
003-002-8126 |     "service": "dd-sanity-check",
003-002-8126 |     "env": "dev",
003-002-8126 |     "version": "",
003-002-8126 |     "language": "javascript"
003-002-8126 |   },
003-002-8126 |   "metrics": {
003-002-8126 |     "_sample_rate": 1.0,
003-002-8126 |     "_sampling_priority_v1": 1.0
003-002-8126 |   }
003-002-8126 | }
004-002-8126 | trace =
004-002-8126 | {
004-002-8126 |   "trace_id": 6094184664711840243,
004-002-8126 |   "span_id": 862068637017604703,
004-002-8126 |   "start": 1600440824029090560,
004-002-8126 |   "duration": 577148,
004-002-8126 |   "error": 0,
004-002-8126 |   "parent_id": 6094184664711840243,
004-002-8126 |   "name": "express.middleware",
004-002-8126 |   "resource": "<anonymous>",
004-002-8126 |   "service": "dd-sanity-check",
004-002-8126 |   "meta": {
004-002-8126 |     "service": "dd-sanity-check",
004-002-8126 |     "env": "dev",
004-002-8126 |     "version": "",
004-002-8126 |     "language": "javascript"
004-002-8126 |   },
004-002-8126 |   "metrics": {
004-002-8126 |     "_sample_rate": 1.0,
004-002-8126 |     "_sampling_priority_v1": 1.0
004-002-8126 |   }
004-002-8126 | }
005-002-8126 | trace =
005-002-8126 | {
005-002-8126 |   "trace_id": 6094184664711840243,
005-002-8126 |   "span_id": 5446107529360283675,
005-002-8126 |   "start": 1600440824030011136,
005-002-8126 |   "duration": 3015869,
005-002-8126 |   "error": 0,
005-002-8126 |   "parent_id": 2378384237909387900,
005-002-8126 |   "name": "express.middleware",
005-002-8126 |   "resource": "catchAllHandler",
005-002-8126 |   "service": "dd-sanity-check",
005-002-8126 |   "meta": {
005-002-8126 |     "service": "dd-sanity-check",
005-002-8126 |     "env": "dev",
005-002-8126 |     "version": "",
005-002-8126 |     "language": "javascript"
005-002-8126 |   },
005-002-8126 |   "metrics": {
005-002-8126 |     "_sample_rate": 1.0,
005-002-8126 |     "_dd.agent_psr": 1.0,
005-002-8126 |     "_sampling_priority_v1": 1.0
005-002-8126 |   }
005-002-8126 | }
006-002-8126 | trace =
006-002-8126 | {
006-002-8126 |   "trace_id": 6094184664711840243,
006-002-8126 |   "span_id": 2378384237909387900,
006-002-8126 |   "start": 1600440824029864704,
006-002-8126 |   "duration": 3169678,
006-002-8126 |   "error": 0,
006-002-8126 |   "parent_id": 6094184664711840243,
006-002-8126 |   "name": "express.middleware",
006-002-8126 |   "resource": "bound dispatch",
006-002-8126 |   "service": "dd-sanity-check",
006-002-8126 |   "meta": {
006-002-8126 |     "service": "dd-sanity-check",
006-002-8126 |     "env": "dev",
006-002-8126 |     "version": "",
006-002-8126 |     "language": "javascript"
006-002-8126 |   },
006-002-8126 |   "metrics": {
006-002-8126 |     "_sample_rate": 1.0,
006-002-8126 |     "_sampling_priority_v1": 1.0
006-002-8126 |   }
006-002-8126 | }
007-002-8126 | trace =
007-002-8126 | {
007-002-8126 |   "trace_id": 6094184664711840243,
007-002-8126 |   "span_id": 6094184664711840243,
007-002-8126 |   "start": 1600440824026759168,
007-002-8126 |   "duration": 7048096,
007-002-8126 |   "error": 0,
007-002-8126 |   "parent_id": 0,
007-002-8126 |   "name": "express.request",
007-002-8126 |   "resource": "GET",
007-002-8126 |   "service": "dd-sanity-check-express",
007-002-8126 |   "type": "web",
007-002-8126 |   "meta": {
007-002-8126 |     "service": "dd-sanity-check",
007-002-8126 |     "env": "dev",
007-002-8126 |     "version": "",
007-002-8126 |     "http.url": "http://localhost:10034/",
007-002-8126 |     "http.method": "GET",
007-002-8126 |     "span.kind": "server",
007-002-8126 |     "http.status_code": "200"
007-002-8126 |   },
007-002-8126 |   "metrics": {
007-002-8126 |     "_sample_rate": 1.0,
007-002-8126 |     "_sampling_priority_v1": 1.0
007-002-8126 |   }
007-002-8126 | }
172.17.0.1 - - [18/Sep/2020 14:53:45] "PUT /v0.4/traces HTTP/1.1" 200 -
005-005-8125 | metric =
005-005-8125 | {
005-005-8125 |   "raw_binary": "ZGQtc2FuaXR5LWNoZWNrLnJlcXVlc3Q6MXxjfCNwYXRoOi8=",
005-005-8125 |   "raw": "dd-sanity-check.request:1|c|#path:/",
005-005-8125 |   "metric": {
005-005-8125 |     "name": "dd-sanity-check.request",
005-005-8125 |     "value": "1"
005-005-8125 |   },
005-005-8125 |   "type": "COUNT",
005-005-8125 |   "tags": [
005-005-8125 |     "path:/"
005-005-8125 |   ]
005-005-8125 | }
006-006-8125 | metric =
006-006-8125 | {
006-006-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX2NvZGUuMjAwOjF8Y3wjcm91dGU6KixtZXRob2Q6R0VULHJlc3BvbnNlX2NvZGU6MjAwLHNlcnZpY2U6ZGQtc2FuaXR5LWNoZWNr",
006-006-8125 |   "raw": "api.requests.response_code.200:1|c|#route:*,method:GET,response_code:200,service:dd-sanity-check",
006-006-8125 |   "metric": {
006-006-8125 |     "name": "api.requests.response_code.200",
006-006-8125 |     "value": "1"
006-006-8125 |   },
006-006-8125 |   "type": "COUNT",
006-006-8125 |   "tags": [
006-006-8125 |     "route:*",
006-006-8125 |     "method:GET",
006-006-8125 |     "response_code:200",
006-006-8125 |     "service:dd-sanity-check"
006-006-8125 |   ]
006-006-8125 | }
007-007-8125 | metric =
007-007-8125 | {
007-007-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX2NvZGUuYWxsOjF8Y3wjcm91dGU6KixtZXRob2Q6R0VULHJlc3BvbnNlX2NvZGU6MjAwLHNlcnZpY2U6ZGQtc2FuaXR5LWNoZWNr",
007-007-8125 |   "raw": "api.requests.response_code.all:1|c|#route:*,method:GET,response_code:200,service:dd-sanity-check",
007-007-8125 |   "metric": {
007-007-8125 |     "name": "api.requests.response_code.all",
007-007-8125 |     "value": "1"
007-007-8125 |   },
007-007-8125 |   "type": "COUNT",
007-007-8125 |   "tags": [
007-007-8125 |     "route:*",
007-007-8125 |     "method:GET",
007-007-8125 |     "response_code:200",
007-007-8125 |     "service:dd-sanity-check"
007-007-8125 |   ]
007-007-8125 | }
008-008-8125 | metric =
008-008-8125 | {
008-008-8125 |   "raw_binary": "YXBpLnJlcXVlc3RzLnJlc3BvbnNlX3RpbWU6MnxofCNyb3V0ZToqLG1ldGhvZDpHRVQscmVzcG9uc2VfY29kZToyMDAsc2VydmljZTpkZC1zYW5pdHktY2hlY2s=",
008-008-8125 |   "raw": "api.requests.response_time:2|h|#route:*,method:GET,response_code:200,service:dd-sanity-check",
008-008-8125 |   "metric": {
008-008-8125 |     "name": "api.requests.response_time",
008-008-8125 |     "value": "2"
008-008-8125 |   },
008-008-8125 |   "type": "HISTOGRAM",
008-008-8125 |   "tags": [
008-008-8125 |     "route:*",
008-008-8125 |     "method:GET",
008-008-8125 |     "response_code:200",
008-008-8125 |     "service:dd-sanity-check"
008-008-8125 |   ]
008-008-8125 | }
008-003-8126 | trace =
008-003-8126 | {
008-003-8126 |   "trace_id": 5256982479716358158,
008-003-8126 |   "span_id": 8051431579635527951,
008-003-8126 |   "start": 1600440843484925952,
008-003-8126 |   "duration": 53223,
008-003-8126 |   "error": 0,
008-003-8126 |   "parent_id": 70930238747602474,
008-003-8126 |   "name": "express.middleware",
008-003-8126 |   "resource": "query",
008-003-8126 |   "service": "dd-sanity-check",
008-003-8126 |   "meta": {
008-003-8126 |     "service": "dd-sanity-check",
008-003-8126 |     "env": "dev",
008-003-8126 |     "version": "",
008-003-8126 |     "language": "javascript"
008-003-8126 |   },
008-003-8126 |   "metrics": {
008-003-8126 |     "_sample_rate": 1.0,
008-003-8126 |     "_sampling_priority_v1": 1.0
008-003-8126 |   }
008-003-8126 | }
009-003-8126 | trace =
009-003-8126 | {
009-003-8126 |   "trace_id": 5256982479716358158,
009-003-8126 |   "span_id": 6527292192246824397,
009-003-8126 |   "start": 1600440843485008128,
009-003-8126 |   "duration": 52734,
009-003-8126 |   "error": 0,
009-003-8126 |   "parent_id": 70930238747602474,
009-003-8126 |   "name": "express.middleware",
009-003-8126 |   "resource": "expressInit",
009-003-8126 |   "service": "dd-sanity-check",
009-003-8126 |   "meta": {
009-003-8126 |     "service": "dd-sanity-check",
009-003-8126 |     "env": "dev",
009-003-8126 |     "version": "",
009-003-8126 |     "language": "javascript"
009-003-8126 |   },
009-003-8126 |   "metrics": {
009-003-8126 |     "_sample_rate": 1.0,
009-003-8126 |     "_sampling_priority_v1": 1.0
009-003-8126 |   }
009-003-8126 | }
010-003-8126 | trace =
010-003-8126 | {
010-003-8126 |   "trace_id": 5256982479716358158,
010-003-8126 |   "span_id": 2627698473297598592,
010-003-8126 |   "start": 1600440843485091072,
010-003-8126 |   "duration": 98877,
010-003-8126 |   "error": 0,
010-003-8126 |   "parent_id": 70930238747602474,
010-003-8126 |   "name": "express.middleware",
010-003-8126 |   "resource": "<anonymous>",
010-003-8126 |   "service": "dd-sanity-check",
010-003-8126 |   "meta": {
010-003-8126 |     "service": "dd-sanity-check",
010-003-8126 |     "env": "dev",
010-003-8126 |     "version": "",
010-003-8126 |     "language": "javascript"
010-003-8126 |   },
010-003-8126 |   "metrics": {
010-003-8126 |     "_sample_rate": 1.0,
010-003-8126 |     "_sampling_priority_v1": 1.0
010-003-8126 |   }
010-003-8126 | }
011-003-8126 | trace =
011-003-8126 | {
011-003-8126 |   "trace_id": 5256982479716358158,
011-003-8126 |   "span_id": 244587645706794221,
011-003-8126 |   "start": 1600440843485272832,
011-003-8126 |   "duration": 458252,
011-003-8126 |   "error": 0,
011-003-8126 |   "parent_id": 3854951892027996367,
011-003-8126 |   "name": "express.middleware",
011-003-8126 |   "resource": "catchAllHandler",
011-003-8126 |   "service": "dd-sanity-check",
011-003-8126 |   "meta": {
011-003-8126 |     "service": "dd-sanity-check",
011-003-8126 |     "env": "dev",
011-003-8126 |     "version": "",
011-003-8126 |     "language": "javascript"
011-003-8126 |   },
011-003-8126 |   "metrics": {
011-003-8126 |     "_sample_rate": 1.0,
011-003-8126 |     "_dd.agent_psr": 1.0,
011-003-8126 |     "_sampling_priority_v1": 1.0
011-003-8126 |   }
011-003-8126 | }
012-003-8126 | trace =
012-003-8126 | {
012-003-8126 |   "trace_id": 5256982479716358158,
012-003-8126 |   "span_id": 3854951892027996367,
012-003-8126 |   "start": 1600440843485235200,
012-003-8126 |   "duration": 501221,
012-003-8126 |   "error": 0,
012-003-8126 |   "parent_id": 70930238747602474,
012-003-8126 |   "name": "express.middleware",
012-003-8126 |   "resource": "bound dispatch",
012-003-8126 |   "service": "dd-sanity-check",
012-003-8126 |   "meta": {
012-003-8126 |     "service": "dd-sanity-check",
012-003-8126 |     "env": "dev",
012-003-8126 |     "version": "",
012-003-8126 |     "language": "javascript"
012-003-8126 |   },
012-003-8126 |   "metrics": {
012-003-8126 |     "_sample_rate": 1.0,
012-003-8126 |     "_sampling_priority_v1": 1.0
012-003-8126 |   }
012-003-8126 | }
013-003-8126 | trace =
013-003-8126 | {
013-003-8126 |   "trace_id": 5256982479716358158,
013-003-8126 |   "span_id": 70930238747602474,
013-003-8126 |   "start": 1600440843484772096,
013-003-8126 |   "duration": 1145752,
013-003-8126 |   "error": 0,
013-003-8126 |   "parent_id": 8812621040420442199,
013-003-8126 |   "name": "express.request",
013-003-8126 |   "resource": "GET",
013-003-8126 |   "service": "dd-sanity-check-express",
013-003-8126 |   "type": "web",
013-003-8126 |   "meta": {
013-003-8126 |     "service": "dd-sanity-check",
013-003-8126 |     "env": "dev",
013-003-8126 |     "version": "",
013-003-8126 |     "http.url": "http://localhost:10034/",
013-003-8126 |     "http.method": "GET",
013-003-8126 |     "span.kind": "server",
013-003-8126 |     "http.status_code": "200"
013-003-8126 |   },
013-003-8126 |   "metrics": {
013-003-8126 |     "_sample_rate": 1.0,
013-003-8126 |     "_sampling_priority_v1": 1.0
013-003-8126 |   }
013-003-8126 | }
172.17.0.1 - - [18/Sep/2020 14:54:05] "PUT /v0.4/traces HTTP/1.1" 200 -
```

[1]: images/screenshot.png
