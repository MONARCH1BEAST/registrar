"""Iterators and generators for Module 2 functional programming.
Classroom yields objects manually; student_rows streams database rows.
"""

from m2_functional.context_meta import DBConnection


# CONCEPT: Iterators
class Classroom:
    """A simple stateful iterator over a classroom list."""

    def __init__(self, students):
        self.students = students
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.position >= len(self.students):
            raise StopIteration
        student = self.students[self.position]
        self.position += 1
        return student


# CONCEPT: Generators and yield
def student_rows():
    """Yield database rows one at a time while the context is open."""
    with DBConnection() as conn:
        cursor = conn.execute("SELECT roll, name, marks FROM students")
        for row in cursor:
            yield dict(row)


def _show_classroom(students):
    classroom = Classroom(students)
    for student in classroom:
        print(student.name)


def _show_manual_iterator():
    manual = Classroom(["first", "second"])
    while True:
        try:
            print("next:", next(manual))
        except StopIteration:
            print("iterator finished")
            break


def _show_student_rows():
    try:
        rows = list(student_rows())
        for row in rows[:3]:
            print(row)
    except Exception as error:
        print("database rows unavailable:", error)


def demo():
    """Use the iterator protocol and consume the row generator fully."""
    from m1_oop.student import Student

    students = [Student(1, "One", 50), Student(2, "Two", 60)]
    _show_classroom(students)
    _show_manual_iterator()
    _show_student_rows()


if __name__ == "__main__":
    demo()
