"""Student, assignment, and submission models for the registrar."""
from m1_oop.person import Person
from m3_data.exceptions import InvalidMarksError

# CONCEPT: Encapsulation, inheritance, and operator overloading
class Student(Person):
    PASS_MARK = 40
    count = 0
    def __init__(self, roll, name, marks=0):
        roll = str(roll).strip()
        if not self.valid_roll(roll): raise ValueError("roll must be a non-empty ID without spaces")
        super().__init__(name); self.roll = roll; self.__marks = None
        self.set_marks(marks); Student.count += 1
    def get_marks(self): return self.__marks
    def set_marks(self, value):
        if not isinstance(value, (int, float)) or not 0 <= value <= 100: raise InvalidMarksError("marks must be between 0 and 100")
        self.__marks = value
    def grade(self): return "Pass" if self.__marks >= self.PASS_MARK else "Fail"
    def to_dict(self): return {"roll": self.roll, "name": self.name, "marks": self.__marks, "grade": self.grade()}
    def show_details(self): return str(self)
    def __str__(self): return "{} {} - {} ({})".format(self.roll, self.name, self.__marks, self.grade())
    def __lt__(self, other): return self.get_marks() < other.get_marks()
    def __add__(self, other): return self.get_marks() + other.get_marks()
    @classmethod
    def from_csv_row(cls, row): return cls(row["roll"], row["name"], float(row["marks"]))
    @staticmethod
    def valid_roll(roll): return isinstance(roll, str) and bool(roll) and roll == roll.strip() and any(char.isalnum() for char in roll) and all(char.isalnum() or char == "-" for char in roll)

class Assignment:
    def __init__(self, title, max_marks, due_date, id=None):
        self.id = id; self.title = title; self.max_marks = max_marks; self.due_date = due_date
    def __str__(self): return "{} ({} marks, due {})".format(self.title, self.max_marks, self.due_date)

class Submission:
    def __init__(self, assignment, student, marks, submitted_on):
        self.assignment = assignment; self.student = student; self.submitted_on = submitted_on; self.__marks = None
        self.set_marks(marks)
    def get_marks(self): return self.__marks
    def set_marks(self, value):
        if not isinstance(value, (int, float)) or not 0 <= value <= self.assignment.max_marks: raise InvalidMarksError("marks must be within the assignment maximum")
        self.__marks = value
    def __str__(self): return "{} (roll {}): {}/{}".format(self.student.name, self.student.roll, self.__marks, self.assignment.max_marks)
    def __lt__(self, other): return self.get_marks() < other.get_marks()

def demo():
    student = Student(101, "Aarav", 78); assignment = Assignment("Python", 100, "2026-11-30")
    submission = Submission(assignment, student, 78, "2026-10-28")
    print(student); print(assignment); print(submission); print("marks:", submission.get_marks())

if __name__ == "__main__": demo()
