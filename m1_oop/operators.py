"""Operator overloading demonstrations for Module 1 OOP.
Student supplies __lt__, __add__, and __str__ for these examples.
"""

# CONCEPT: Operator overloading
from m1_oop.student import Student


def demo():
    """Show sorting, maximum selection, addition, and string conversion."""
    students = [
        Student(101, "Aarav", 78),
        Student(102, "Diya", 35),
        Student(103, "Rohan", 92),
    ]
    print("sorted:", [student.roll for student in sorted(students)])
    print("highest:", max(students))
    print("combined marks:", students[0] + students[1])
    print("as text:", str(students[2]))


if __name__ == "__main__":
    demo()
