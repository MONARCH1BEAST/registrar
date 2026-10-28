"""TCP client requests for Module 4 networking practice.
Module 4 demonstrates connecting, sending a line, receiving a line, and closing.
"""

# CHANGE ME: the client reads the shared endpoint from settings.py.

import socket

import settings


# CONCEPT: Socket programming
def _receive_reply(sock):
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8", errors="replace").split("\n", 1)[0]


def send_command(text):
    """Send one newline-terminated command and return one newline-free reply."""
    try:
        with socket.create_connection((settings.HOST, settings.SOCKET_PORT)) as sock:
            # The newline tells the server where this text request ends.
            sock.sendall((text.rstrip("\r\n") + "\n").encode("utf-8"))
            return _receive_reply(sock)
    except ConnectionRefusedError:
        return "ERROR|Server is not running"
    except OSError:
        return "ERROR|Could not connect to server"


def demo():
    """Read commands until the user types quit."""
    while True:
        text = input("Command (RESULT 101, COUNT, or quit): ")
        if text.lower() == "quit":
            break
        print(send_command(text))


if __name__ == "__main__":
    demo()
