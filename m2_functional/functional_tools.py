"""Higher-order functions and recursion for Module 2 functional programming.
These small functions operate on student-like objects by duck typing.
"""

from functools import reduce


# CONCEPT: Higher-order functions
def apply_to_all(items, func):
    """Apply a supplied function to each item with a plain loop."""
    results = []
    for item in items:
        results.append(func(item))
    return results


def _add_grace_to_student(student):
    marks = min(100, student.get_marks() + GRACE_MARKS)
    student.set_marks(marks)
    return student


GRACE_MARKS = 5  # CHANGE ME: grace marks


# CONCEPT: Lambda functions
# CONCEPT: map(), filter(), reduce()
def add_grace(students):
    """Use map and a lambda to add capped grace marks."""
    return list(map(lambda student: _add_grace_to_student(student), students))


def failed_students(students):
    """Use filter to keep students whose grade is Fail."""
    return list(filter(lambda student: student.grade() == "Fail", students))


def class_total(students):
    """Use reduce to fold all marks into one total."""
    return reduce(lambda total, student: total + student.get_marks(), students, 0)


def sort_students(students, key):
    """Wrap sorted so callers choose the ordering key."""
    return sorted(students, key=key)


# CONCEPT: Recursive functions
def total_marks(node):
    """Recursively total students in nested dictionaries and lists."""
    if isinstance(node, list):
        return class_total(node)
    if isinstance(node, dict):
        total = 0
        for value in node.values():
            total += total_marks(value)
        return total
    return 0


def _build_aiml_groups(Student):
    return {
        "Sem3-A": [
            Student(101, "Aarav", 78),
            Student(102, "Diya", 35),
            Student(103, "Rohan", 92),
        ],
        "Sem3-B": [
            Student(104, "Sneha", 56),
            Student(105, "Kabir", 40),
            Student(106, "Meera", 28),
        ],
    }


def _build_ds_groups(Student):
    return {
        "Sem3-A": [
            Student(107, "Arjun", 67),
            Student(108, "Isha", 85),
            Student(109, "Vikram", 49),
            Student(110, "Ananya", 39),
        ],
    }


def _build_groups(Student):
    return {
        "AIML": _build_aiml_groups(Student),
        "DS": _build_ds_groups(Student),
    }


def _flatten_groups(groups):
    all_students = []
    for branch in groups.values():
        for section in branch.values():
            for student in section:
                all_students.append(student)
    return all_students


def _copy_students(students, Student):
    copies = []
    for student in students:
        copies.append(Student(student.roll, student.name, student.get_marks()))
    return copies


def demo():
    """Build nested class groups and verify the expected total of 569."""
    from m1_oop.student import Student

    groups = _build_groups(Student)
    all_students = _flatten_groups(groups)
    print("failed at pass mark 40:", len(failed_students(all_students)))
    grace_students = _copy_students(all_students, Student)
    add_grace(grace_students)
    print("grace total:", class_total(grace_students))
    print("nested total:", total_marks(groups))
    print("recursive total:", total_marks(groups))
    print("expected:", 569)


if __name__ == "__main__":
    demo()
