"""Custom exceptions and assertions for Module 3: File Handling, Exceptions and Database Connectivity.
This module keeps user-facing error names small and meaningful.
"""

# CHANGE ME: add another named exception here when a new error needs to be taught.

# CONCEPT: User-defined exceptions


class InvalidMarksError(Exception):
    """Marks must be between zero and one hundred."""


class StudentNotFoundError(Exception):
    """No student exists for the requested roll number."""


def check_marks(marks):
    # CONCEPT: Assertions
    # Assertions document programmer assumptions; user input needs a real exception.
    assert 0 <= marks <= 100, "marks out of range"


def _show_assertion_example():
    try:
        check_marks(150)
    except AssertionError as error:
        print("Assertion caught:", error)
    finally:
        print("The assertion example always reaches finally.")


def _show_invalid_marks_example():
    try:
        raise InvalidMarksError("marks must be between 0 and 100")
    except InvalidMarksError as error:
        print("InvalidMarksError caught:", error)
    finally:
        print("Invalid marks cleanup is complete.")


def _show_missing_student_example():
    try:
        raise StudentNotFoundError("student 999 was not found")
    except StudentNotFoundError as error:
        print("StudentNotFoundError caught:", error)
    finally:
        print("Missing-student cleanup is complete.")


def demo():
    """Show an assertion and two user-defined exceptions."""
    _show_assertion_example()
    _show_invalid_marks_example()
    _show_missing_student_example()
    print("Assertions suit programmer mistakes; exceptions suit bad user input.")


if __name__ == "__main__":
    demo()
