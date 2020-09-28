import flask
import msgpack

import counter
import pretty_json


REQUEST_COUNTER = counter.Counter()
TRACE_COUNTER = counter.Counter()
APP = flask.Flask(__name__)
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


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

    return flask.jsonify({})


if __name__ == "__main__":
    APP.run()
