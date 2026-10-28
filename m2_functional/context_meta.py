"""Context managers and metaclasses for Module 2 advanced functions.
DBConnection owns SQLite cleanup; RegistryMeta records defined classes.
"""

from abc import ABCMeta
import sqlite3

import settings


# CONCEPT: Context managers
class DBConnection:
    """Commit successful work, roll back errors, and always close SQLite."""

    def __init__(self, db_name=settings.DB_NAME):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        return False


# CONCEPT: Metaclasses
class RegistryMeta(ABCMeta):
    """Register each class at the moment its definition is completed."""

    registry = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        RegistryMeta.registry[name] = cls


def _load_oop_class_names():
    from m2_functional.context_meta import RegistryMeta as LoadedRegistryMeta
    from m1_oop.person import Person
    from m1_oop.student import Student
    from m1_oop.special import PGStudent, Teacher, TeachingAssistant

    # These imports ensure the demo shows the complete OOP hierarchy.
    classes = [
        Person.__name__,
        Student.__name__,
        Teacher.__name__,
        PGStudent.__name__,
        TeachingAssistant.__name__,
    ]
    return LoadedRegistryMeta, classes


def demo():
    """Open a connection and display classes known to the metaclass."""
    with DBConnection() as conn:
        conn.execute("SELECT 1")
        print("connection opened")
    loaded_meta, classes = _load_oop_class_names()
    print("registered:", sorted(loaded_meta.registry))
    print("classes:", classes)


if __name__ == "__main__":
    demo()
