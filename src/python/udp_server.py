import os
import socketserver

import counter
import parse_datagram
import pretty_json


COUNTER = counter.Counter()
HOST = "0.0.0.0"
METRICS_PORT = int(os.environ.get("METRICS_PORT", 8125))


class Handler(socketserver.BaseRequestHandler):

    PREFIX_SUFFIX = METRICS_PORT

    def handle(self):
        count = COUNTER.increment()
        # There is no difference between request count / metric count as there
        # is for the trace server.
        prefix = f"{count:03d}-{count:03d}-{self.PREFIX_SUFFIX} | "

        data = self.request[0].strip()
        data_parsed = parse_datagram.parse_metric(data)
        try:
            colorful_json = pretty_json.printable_json(data_parsed, prefix)

            print(f"{prefix}metric =")
            print(colorful_json, end="")
        except:
            print(f"{prefix}metric raw data = {data_parsed!r}")


def main():
    print(f"Starting UDP metrics server on {HOST}:{METRICS_PORT}")
    with socketserver.UDPServer((HOST, METRICS_PORT), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
