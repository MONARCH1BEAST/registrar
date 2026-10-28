"""TCP sockets and a thread-per-client server for Module 4 networking.
Module 4 demonstrates line protocols, client threads, and safe connection closing.
"""

# CHANGE ME: the server uses the shared host and socket port in settings.py.

import socket
import threading

import settings
from m3_data import database


# CONCEPT: Socket programming
def _grade_for(marks):
    """Use the student model's pass mark without making a student object."""
    try:
        from m1_oop.student import Student
        pass_mark = Student.PASS_MARK
    except ImportError:
        pass_mark = 40
    if float(marks) >= pass_mark:
        return "Pass"
    return "Fail"


def _result_reply(parts):
    """Build a RESULT reply, or return None for another command."""
    if len(parts) != 2 or parts[0] != "RESULT":
        return None
    student, error_reply = _lookup_student(parts[1])
    if error_reply is not None:
        return error_reply
    grade = _grade_for(student["marks"])
    return "OK|%s|%s|%s|%s" % (
        student["roll"], student["name"], student["marks"], grade)


def _lookup_student(roll_text):
    """Look up a roll number and return a protocol error when needed."""
    try:
        student = database.get_student(roll_text)
        if student is None: return None, "ERROR|Student %s not found" % roll_text
    except Exception as error:
        if error.__class__.__name__ == "StudentNotFoundError":
            return None, "ERROR|Student %s not found" % roll_text
        return None, "ERROR|Server error"
    return student, None


# CONCEPT: Client-server communication
def handle_command(line):
    """Return one protocol reply for one request without a trailing newline."""
    line = line.strip()
    if line == "COUNT":
        return "OK|%d" % len(database.get_all_students())
    if line == "QUIT":
        return "OK|bye"
    reply = _result_reply(line.split())
    if reply is not None:
        return reply
    return "ERROR|Unknown command"


def _process_pending(conn, pending):
    """Send replies for complete lines and report whether QUIT was received."""
    while "\n" in pending:
        line, pending = pending.split("\n", 1)
        reply = handle_command(line)
        conn.sendall((reply + "\n").encode("utf-8"))
        if line.strip() == "QUIT":
            return pending, True
    return pending, False


def _read_pending(conn, pending):
    """Read one socket chunk and indicate whether data was received."""
    data = conn.recv(1024)
    if not data:
        return pending, False
    return pending + data.decode("utf-8", errors="replace"), True


def handle_client(conn, addr):
    """Serve complete newline-terminated requests and always close the socket."""
    pending = ""
    try:
        while True:
            pending, has_data = _read_pending(conn, pending)
            if not has_data:
                break
            pending, should_stop = _process_pending(conn, pending)
            if should_stop:
                return
    except (ConnectionError, OSError):
        return
    finally:
        conn.close()


def _make_server_socket():
    """Create, configure, and bind the listening socket."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((settings.HOST, settings.SOCKET_PORT))
        server_socket.listen()
    except BaseException:
        server_socket.close()
        raise
    return server_socket


def _accept_clients(server_socket):
    """Accept clients and start one daemon worker for each connection."""
    print("Listening on %s:%s" % (settings.HOST, settings.SOCKET_PORT))
    while True:
        conn, addr = server_socket.accept()
        worker = threading.Thread(target=handle_client, args=(conn, addr))
        worker.daemon = True
        worker.start()


def start_server():
    """Bind the configured TCP port and start one daemon thread per client."""
    database.create_table()
    database.seed_from_csv()
    server_socket = None
    try:
        server_socket = _make_server_socket()
        _accept_clients(server_socket)
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        if server_socket is not None:
            server_socket.close()


def demo():
    """Start the blocking server only when this demo is explicitly selected."""
    start_server()


if __name__ == "__main__":
    demo()
