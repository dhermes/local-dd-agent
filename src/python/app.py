import json

import flask
import msgpack

import counter
import pretty_json


REQUEST_COUNTER = counter.Counter()
TRACE_COUNTER = counter.Counter()
APP = flask.Flask(__name__)
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
CONTENT_TYPE_MSGPACK = "application/msgpack"
CONTENT_TYPE_JSON = "application/json"


def _flatten_traces(data_parsed):
    # Flatten from the "outside"
    if len(data_parsed) == 1:
        return data_parsed[0]

    # Flatten from the "inside"
    if all(len(value) == 1 for value in data_parsed):
        return [value[0] for value in data_parsed]

    # Do nothing
    return data_parsed


@APP.route("/", defaults={"path": ""}, methods=METHODS)
@APP.route("/<path:path>", methods=METHODS)
def catch_all(path):
    request_count = REQUEST_COUNTER.increment()

    content_type = flask.request.content_type
    data = flask.request.get_data()
    try:
        if content_type == CONTENT_TYPE_MSGPACK:
            data_parsed = msgpack.loads(data)
        elif content_type == CONTENT_TYPE_JSON:
            data_parsed = json.loads(data)
        else:
            raise ValueError("Unexpected content type", content_type)

        traces = _flatten_traces(data_parsed)
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

    return flask.jsonify({})


if __name__ == "__main__":
    APP.run()
