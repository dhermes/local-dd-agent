import flask
import msgpack

import counter
import pretty_json


REQUEST_COUNTER = counter.Counter()
TRACE_COUNTER = counter.Counter()
APP = flask.Flask(__name__)
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
RESPONSE_HTML = """\
<html>
  <head>
    <title>Hello</title>
  </head>
  <body>
    <h1>Hello</h1>
  </body>
</html>
"""


@APP.route("/", defaults={"path": ""}, methods=METHODS)
@APP.route("/<path:path>", methods=METHODS)
def catch_all(path):
    request_count = REQUEST_COUNTER.increment()

    data = flask.request.get_data()
    try:
        data_parsed = msgpack.loads(data)
        (traces,) = data_parsed  # Assert one entry

        for trace in traces:
            trace_count = TRACE_COUNTER.increment()
            prefix = f"{trace_count:03d}-{request_count:03d}-8126 | "
            colorful_json = pretty_json.printable_json(trace, prefix)
            print(f"{prefix}trace =")
            print(colorful_json, end="")
    except:
        trace_count = TRACE_COUNTER.increment()
        prefix = f"{trace_count:03d}-{request_count:03d}-8126 | "
        print(f"{prefix}trace raw data = {data!r}")

    response = flask.Response(RESPONSE_HTML)
    response.headers["content-type"] = "application/html"
    return response


if __name__ == "__main__":
    APP.run()
