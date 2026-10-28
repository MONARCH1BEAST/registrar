"""Decorators for logging, timing, and access control in Module 2.
Each wrapper adds one behaviour while preserving the wrapped function.
"""

import functools
import logging
import time


CURRENT_ROLE = "admin"  # CHANGE ME: current role
logger = logging.getLogger("srm")


# CONCEPT: Decorators
def log_action(func):
    """Log the wrapped function name through the shared srm logger."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("%s called", func.__name__)
        return func(*args, **kwargs)
    return wrapper


def timer(func):
    """Print the elapsed time for one call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - started
        print(func.__name__, "took", round(elapsed, 6), "seconds")
        return result
    return wrapper


def admin_only(func):
    """Allow a call only when the module's current role is admin."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if CURRENT_ROLE != "admin":
            raise PermissionError("admin role required")
        return func(*args, **kwargs)
    return wrapper


def _make_demo_actions():
    @log_action
    def add_event(text):
        print("event:", text)

    @timer
    def count_items(items):
        return len(items)

    @admin_only
    def remove_event():
        return "removed"

    return add_event, count_items, remove_event


def _show_denied_action(remove_event):
    global CURRENT_ROLE
    CURRENT_ROLE = "guest"
    try:
        remove_event()
    except PermissionError as error:
        print("blocked:", error)
    CURRENT_ROLE = "admin"


def demo():
    """Run three decorated functions and demonstrate a denied role."""
    add_event, count_items, remove_event = _make_demo_actions()
    add_event("demo started")
    print("item count:", count_items([1, 2, 3]))
    print(remove_event())
    _show_denied_action(remove_event)


if __name__ == "__main__":
    demo()
