"""MySQL connectivity introduction for Module 3: File Handling, Exceptions and Database Connectivity.
The optional demo never makes the rest of the project depend on a MySQL installation.
"""

import settings

# CHANGE ME: edit the shared settings.MYSQL values, not this demo's SQL.

# CONCEPT: Introduction to MySQL


def _load_connector():
    try:
        import mysql.connector
    except ImportError:
        print("MySQL package not installed, skipping")
        return None
    return mysql.connector


def _create_students_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS students (
            roll INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            marks REAL NOT NULL
        )"""
    )


def _print_students(cursor):
    cursor.execute("SELECT roll, name, marks FROM students")
    for row in cursor.fetchall():
        print(row)


def _close_resources(cursor, connection):
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()


def _run_demo(connector):
    connection = None
    cursor = None
    try:
        connection = connector.connect(**settings.MYSQL)
        cursor = connection.cursor()
        _create_students_table(cursor)
        _print_students(cursor)
    except connector.Error:
        print("MySQL server not reachable, skipping")
    finally:
        _close_resources(cursor, connection)


def demo():
    """Connect, query, and close a MySQL database when the optional package is available."""
    connector = _load_connector()
    if connector is not None:
        _run_demo(connector)


if __name__ == "__main__":
    demo()
