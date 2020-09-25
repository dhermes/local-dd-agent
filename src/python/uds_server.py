import os
import pathlib
import socketserver

import counter
import parse_datagram
import pretty_json
import udp_server


COUNTER = counter.Counter()
UDS_PATH = os.environ.get("UDS_PATH", "/var/run/datadog/dsd.socket")


class Handler(udp_server.Handler):

    PREFIX_SUFFIX = "UDS "


def clear_path(uds_path):
    path = pathlib.Path(uds_path)
    try:
        path.unlink()
    except FileNotFoundError:
        if path.exists():
            raise

    path.parent.mkdir(parents=True, exist_ok=True)


def main():
    clear_path(UDS_PATH)
    print(f"Starting UDS metrics server at {UDS_PATH!r}")
    with socketserver.UnixDatagramServer(UDS_PATH, Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
