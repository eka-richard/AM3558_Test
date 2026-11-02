"""Print incoming UTF-8 TCP data, serving one connection at a time.

Usage: py -3 tcp_listener.py 0.0.0.0 5000
Use a local interface's IPv4 address to listen only on that interface.
TCP is a byte stream: received chunks do not define message boundaries.
This listener prints data only; it does not send responses.
"""

import argparse
import codecs
import ipaddress
import socket
import sys


def port_number(value):
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ip", type=ipaddress.IPv4Address, help="Local IPv4 address")
    parser.add_argument("port", type=port_number, help="Local TCP port (1-65535)")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((str(args.ip), args.port))
            server.listen()
            print(f"Listening on {args.ip}:{args.port} (Ctrl+C to stop)", flush=True)

            while True:
                connection, address = server.accept()
                with connection:
                    print(f"\nConnected: {address[0]}:{address[1]}", flush=True)
                    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
                    try:
                        while True:
                            data = connection.recv(4096)
                            if not data:
                                break
                            print(decoder.decode(data), end="", flush=True)
                    except OSError as error:
                        print(f"\nReceive error from {address}: {error}", file=sys.stderr)
                    finally:
                        print(decoder.decode(b"", final=True), end="", flush=True)
                    print("\nConnection closed.", flush=True)
    except KeyboardInterrupt:
        print("\nStopped.")
    except OSError as error:
        print(f"Listener error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
