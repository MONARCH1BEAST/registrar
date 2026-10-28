"""Inheritance types and polymorphism for Module 1 OOP.
Teacher, PGStudent, and TeachingAssistant extend the record classes.
"""

from m1_oop.person import Person
from m1_oop.student import Student


# CONCEPT: Inheritance and its types
class Teacher(Person):
    """A person who teaches one subject."""

    def __init__(self, name, subject="General"):
        super().__init__(name)
        self.subject = subject

    # CONCEPT: Polymorphism
    def show_details(self):
        return "Teacher %s - %s" % (self.name, self.subject)


class PGStudent(Student):
    """A Student extended with a thesis topic."""

    def __init__(self, roll, name, marks, thesis):
        super().__init__(roll, name, marks)
        self.thesis = thesis

    def show_details(self):
        return "PGStudent %s - thesis: %s" % (self.name, self.thesis)


class TeachingAssistant(Student, Teacher):
    """A multiple-inheritance example combining student and teacher roles."""

    def __init__(self, roll, name, marks, subject):
        Student.__init__(self, roll, name, marks)
        self.subject = subject

    def show_details(self):
        return "TeachingAssistant %s - %s" % (self.name, self.subject)


def demo():
    """Call one common method on objects from the inheritance hierarchy."""
    people = [
        Teacher("Dr. Rao", "Python"),
        Student(101, "Aarav", 78),
        PGStudent(201, "Mira", 88, "Data ethics"),
        TeachingAssistant(301, "Kabir", 81, "Algorithms"),
    ]
    for person in people:
        print(person.show_details())
    print("TeachingAssistant MRO:", TeachingAssistant.__mro__)
    print("The MRO resolves the diamond through Person once.")


if __name__ == "__main__":
    demo()
