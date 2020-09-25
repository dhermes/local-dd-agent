"""Forward one socket to another.

The server socket is a UDS (Unix Domain Socket) speaking UDP and the client
socket is a INET socket speaking UDP.

H/T: https://stackoverflow.com/a/23731713/1068170
"""

import os
import pathlib
import select
import signal
import socket

import uds_server


DATADOG_HOSTNAME = os.environ.get("DATADOG_HOSTNAME", "localhost")
DATADOG_PORT = int(os.environ.get("DATADOG_PORT", 8125))
DATADOG_ADDRESS = os.environ.get("DATADOG_ADDRESS")


def _try_remove_uds():
    # Try to remove the UDS.
    path = pathlib.Path(DATADOG_ADDRESS)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def _signal_handler(signal_number, unused_frame):
    signal_pretty = signal_number
    if signal_number == signal.SIGTERM:
        signal_pretty = "SIGTERM"
    elif signal_number == signal.SIGINT:
        signal_pretty = "SIGINT"

    print(f"Handling shutdown signal ({signal_pretty}) for UDS->UDP forwarder")
    _try_remove_uds()


def _recv_all(reader, writer):
    data = b""
    chunk = reader.read(4096)
    while len(chunk) == 4096:
        data += chunk
        chunk = reader.read(4096)
    # Add the last chunk
    data += chunk

    writer.write(data)


def read_loop(server_socket, client_socket):
    server_reader = server_socket.makefile(mode="rb", buffering=False)
    server_writer = server_socket.makefile(mode="wb", buffering=False)
    client_reader = client_socket.makefile(mode="rb", buffering=False)
    client_writer = client_socket.makefile(mode="wb", buffering=False)

    rlist = (client_reader, server_reader)
    wlist = ()
    xlist = ()
    while True:
        ready_rlist, _, _ = select.select(rlist, wlist, xlist)
        for ready_socket in ready_rlist:
            if ready_socket == server_reader:
                _recv_all(server_reader, client_writer)
            elif ready_socket == client_reader:
                _recv_all(client_reader, server_writer)


def main():
    # Register signal handlers.
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    uds_server.clear_path(DATADOG_ADDRESS)
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_socket.bind(DATADOG_ADDRESS)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((DATADOG_HOSTNAME, DATADOG_PORT))

    try:
        read_loop(server_socket, client_socket)
    except ConnectionRefusedError:
        print("Server is no longer running")
    finally:
        _try_remove_uds()


if __name__ == "__main__":
    main()
