"""Variable scope, closures, and dynamic typing for Module 2.
The examples show global, local, nonlocal, and changing value types.
"""


# CONCEPT: Scope and lifetime of variables
session_count = 0


def open_session():
    """Update the module-level session counter."""
    global session_count
    session_count += 1
    return session_count


def make_counter():
    """Return a closure whose private count survives each call."""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


# CONCEPT: Dynamic typing
def normalise_roll(value):
    """Convert listed whole-number forms to an integer roll."""
    if isinstance(value, bool):
        raise ValueError("roll must be a positive whole number")
    if isinstance(value, int):
        roll = value
    elif isinstance(value, float) and value.is_integer():
        roll = int(value)
    elif isinstance(value, str) and value.strip().isdigit():
        roll = int(value.strip())
    else:
        raise ValueError("roll must be a positive whole number")
    if roll <= 0:
        raise ValueError("roll must be a positive whole number")
    return roll


def _make_local():
    local_value = "inside the function"
    return local_value


def _show_roll_forms(values):
    for value in values:
        try:
            print(value, "->", normalise_roll(value))
        except ValueError as error:
            print(value, "->", error)


def demo():
    """Display local lifetime, changing types, and accepted roll values."""
    print("local while running:", _make_local())
    print("local disappears after the function returns")
    value = 5
    print(value, type(value))
    value = "five"
    print(value, type(value))
    print("session:", open_session())
    counter = make_counter()
    print("closure:", counter(), counter())
    _show_roll_forms([101, "101", "101 ", 101.0, "bad"])


if __name__ == "__main__":
    demo()
