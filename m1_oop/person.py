"""Abstract classes, constructors, and destructors for Module 1 OOP.
This file demonstrates the Person abstraction used by the student records.
"""

from abc import abstractmethod

from m2_functional.context_meta import RegistryMeta


# CONCEPT: Abstraction and abstract classes
class Person(metaclass=RegistryMeta):
    """An abstract person with a name shared by concrete record types."""

    verbose = False

    # CONCEPT: Constructors and destructors
    def __init__(self, name):
        self.name = name

    def __del__(self):
        # Quiet destruction keeps normal GUI and web runs free of console noise.
        if Person.verbose:
            print("record closed for " + self.name)

    @abstractmethod
    def show_details(self):
        """Return details so every concrete person presents itself."""
        pass


def _show_abstract_error():
    try:
        Person("x")
    except TypeError as error:
        print("abstract class:", error)


def _show_destructor():
    class DemoPerson(Person):
        def show_details(self):
            return "demo person: " + self.name

    Person.verbose = True
    obj = DemoPerson("temporary")
    print(obj.show_details())
    del obj
    Person.verbose = False


def demo():
    """Show abstraction and the optional destructor message."""
    _show_abstract_error()
    _show_destructor()


if __name__ == "__main__":
    demo()
