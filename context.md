# context.md: Student Record Manager

**Course:** Advanced Python Programming (CSG5.03003), Universal Ai University, School of AI & Future Technologies
**Programme / Sem / Year:** AIML/DS, Semester III, 2026-27
**Load:** 2 credits, 2 practical hours per week, five modules of 12 hours each (CO1 to CO5)

> This file is the single source of truth for the project. Use it three ways:
> 1. **Build spec:** every file, function, port, table, and message format is defined here.
> 2. **Revision sheet:** every syllabus topic has a one-line explanation you can say aloud.
> 3. **Prompt for an AI assistant:** paste it in and ask for one module at a time (see section 17).

---

## 1. Project summary

A small system for managing student records. Staff use a **Tkinter desktop window**, students check results on a **Flask web page**, and other programs talk to it through a **socket server** and a **REST API**. All of them share **one SQLite file**, so the CRUD logic is written once.

**Why this project:** everyone already understands "a student with marks", so all your explaining time goes to Python concepts, not the domain. The logic is only add, search, grade, and report.

### Success criteria

1. Every topic from all five modules appears in running code and can be found by searching its `# CONCEPT:` tag.
2. You can open any file and explain it in under one minute.
3. Any change in the cheat sheet (section 11) takes under two minutes.
4. Every file runs on its own with `python -m package.file`.

### Non-goals (do not build these)

Login or security hardening, user roles beyond a simple decorator demo, fancy UI styling, async code, ORMs, a test framework (use the manual checkpoints in section 10).

---

## 2. Coding rules (apply to every file)

1. **One concept per file, about 60 lines.** GUI and web files may reach about 90.
2. **Plain code only.** No walrus operator, no nested comprehensions, no one-line tricks, no type hints. You must be able to explain every line.
3. **File header:** a 2-line docstring naming the concept and the syllabus module.
4. **Settings live in two places:**
   - shared values (ports, file paths, flags) in root `settings.py`
   - file-specific values in a `# CHANGE ME:` block at the top of that file
5. **Every file exposes `demo()`** and ends with `if __name__ == "__main__": demo()`.
6. **Comments explain why**, in plain English, not what the line does.
7. **Functions stay under about 15 lines.**
8. **`__init__.py` files are empty.** Importing one module must never trigger another.
9. **Layer rule (section 5):** a file may import only from lower layers. Exception: `demo()` may import from higher layers *inside the function body*.
10. **Run everything from the project root** (`student_manager/`) so the relative paths in `settings.py` work.
11. **Friendly errors:** catch exceptions where the user sees them (GUI, web, server) and show a plain message. Log the technical detail.
12. **Parameterised SQL only** (`?` placeholders), never string-built queries.

### Search tags (put these in comments so you can find things fast)

| Tag | Meaning | Example |
|---|---|---|
| `# CONCEPT: <name>` | Marks the exact lines showing a syllabus topic | `# CONCEPT: Encapsulation` |
| `# CHANGE ME:` | An easy edit point for live changes | `# CHANGE ME: pass mark` |
| `# ADD FIELD HERE` | Every place that must change when a new student field is added | see section 11 |

If the professor asks "where is polymorphism?", search `CONCEPT: Polymorphism` and you are there.

---

## 3. Setup and run

**Python 3.10 or newer.**

```
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # macOS / Linux
pip install -r requirements.txt
```

`requirements.txt`:

```
flask
requests
beautifulsoup4
mysql-connector-python    # optional, only for m3_data/mysql_demo.py
```

- **Tkinter** ships with Python on Windows and macOS. On Ubuntu/Debian: `sudo apt install python3-tk`.
- Everything else is the standard library.

### Run commands (from the project root)

| What | Command |
|---|---|
| Menu of all demos | `python main.py` |
| Any single file | `python -m m2_functional.decorators` |
| Create and seed the database | `python -m m3_data.database` |
| Socket server (terminal 1) | `python -m m4_network.server` |
| Socket client (terminal 2) | `python -m m4_network.client` |
| Desktop app | `python -m m5_apps.gui` |
| Web app | `python -m m5_apps.web` then open `http://localhost:5001` (binds to `127.0.0.1`; `PORT` is ignored) |

Use `python -m package.file`, not `python package/file.py`, because the files import each other by package name.

---

## 4. Project structure

```
student_manager/
├── main.py                    # menu: pick a number to run any demo
├── settings.py                # shared constants (ports, paths, flags)
├── requirements.txt
├── context.md                 # this file
├── data/
│   ├── sample_students.csv    # 10 seed students (section 6.2)
│   └── config.json            # {"school": "...", "year": "2026-27"}
│   # created at runtime: students.db, activity.txt, app.log,
│   # backup.pkl, export.csv, results.json, report.txt
│
├── m1_oop/                    # MODULE 1: Object-Oriented Programming
│   ├── __init__.py
│   ├── person.py              # abstract Person, constructor, destructor
│   ├── student.py             # Student: class vs instance vars, encapsulation, methods
│   ├── special.py             # Teacher, PGStudent, TeachingAssistant (inheritance types)
│   └── operators.py           # demo of __lt__, __add__
│
├── m2_functional/             # MODULE 2: Advanced Functions
│   ├── __init__.py
│   ├── functional_tools.py    # lambda, higher-order, map/filter/reduce, recursion
│   ├── iterators_gens.py      # iterator class, generator with yield
│   ├── decorators.py          # @log_action, @timer, @admin_only
│   ├── context_meta.py        # DBConnection (context manager), RegistryMeta (metaclass)
│   └── scope_demo.py          # global, nonlocal, dynamic typing
│
├── m3_data/                   # MODULE 3: Files, Exceptions, Database
│   ├── __init__.py
│   ├── exceptions.py          # custom exceptions + assertion
│   ├── logger.py              # logging setup
│   ├── files.py               # text, binary (pickle), CSV, JSON
│   ├── database.py            # SQLite CRUD
│   └── mysql_demo.py          # short MySQL connection demo
│
├── m4_network/                # MODULE 4: Threads, Networking, APIs
│   ├── __init__.py
│   ├── threads.py             # Thread, Lock, Process
│   ├── server.py              # socket server, one thread per client
│   ├── client.py              # socket client
│   └── web_tools.py           # requests, BeautifulSoup, email
│
└── m5_apps/                   # MODULE 5: GUI and Web
    ├── __init__.py
    ├── gui.py                 # Tkinter window
    ├── web.py                 # Flask routes + REST API
    └── templates/
        ├── base.html
        ├── index.html
        ├── student.html
        └── add.html
```

---

## 5. Layers (who may import whom)

```
settings.py
    ↓
m3_data/exceptions.py   m3_data/logger.py
    ↓
m2_functional/*          (context_meta uses settings only)
    ↓
m1_oop/*
    ↓
m3_data/database.py   m3_data/files.py
    ↓
m4_network/*
    ↓
m5_apps/*

main.py imports lazily (inside a function) so a missing optional package never breaks the menu.
```

**Rule:** a file imports only from layers above it in this diagram (the layers it depends on). The `m2` files work on student objects through duck typing (`s.get_marks()`), so they never import `Student`.

---

## 6. Shared contracts

### 6.1 `settings.py`

```python
# Paths (relative to project root)
DB_NAME       = "data/students.db"
LOG_FILE      = "data/app.log"
ACTIVITY_FILE = "data/activity.txt"
CSV_IMPORT    = "data/sample_students.csv"
CSV_EXPORT    = "data/export.csv"
JSON_FILE     = "data/results.json"
CONFIG_FILE   = "data/config.json"
BACKUP_FILE   = "data/backup.pkl"
REPORT_FILE   = "data/report.txt"

# Network
HOST        = "127.0.0.1"
SOCKET_PORT = 5050     # socket server
FLASK_PORT  = 5001     # not 5000: macOS AirPlay uses 5000, and it avoids clashes

# Background work
BACKUP_INTERVAL = 30   # seconds between automatic backups

# Email (password is NEVER stored here; read env var SRM_EMAIL_PASSWORD)
EMAIL_TEST_MODE = True            # True = print the email instead of sending
EMAIL_FROM = "you@example.com"
EMAIL_TO   = "parent@example.com"
SMTP_HOST  = "smtp.gmail.com"
SMTP_PORT  = 587

# MySQL (optional demo)
MYSQL = {"host": "localhost", "user": "root", "password": "", "database": "srm"}

# Scraping practice site (built for scraping)
BOOKS_URL = "http://books.toscrape.com/"
```

### 6.2 Sample data: `data/sample_students.csv`

```
roll,name,marks
101,Aarav Sharma,78
102,Diya Patel,35
103,Rohan Mehta,92
104,Sneha Iyer,56
105,Kabir Singh,40
106,Meera Nair,28
107,Arjun Rao,67
108,Isha Gupta,85
109,Vikram Joshi,49
110,Ananya Das,39
```

The data includes boundary cases (40 and 39, 49) so a pass-mark change is visible immediately.

**Expected values (use these to check your code):**

| Check | Result |
|---|---|
| Student count | 10 |
| Class total / average | 569 / 56.9 |
| Highest | 103 Rohan Mehta (92) |
| Fails when `PASS_MARK = 40` | 102, 106, 110 (3 fail, 7 pass) |
| Fails when `PASS_MARK = 50` | 102, 105, 106, 109, 110 (5 fail, 5 pass) |
| Total after +5 grace marks (cap 100) | 619 |
| A/B/C/Fail with A>=75, B>=60, C>=PASS_MARK | A: 101, 103, 108; B: 107; C: 104, 105, 109; Fail: 102, 106, 110 |

### 6.3 Database schema (SQLite)

```sql
CREATE TABLE batches (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    year TEXT NOT NULL
);

CREATE TABLE students (
    roll     TEXT PRIMARY KEY,
    name     TEXT NOT NULL,
    batch_id INTEGER NOT NULL REFERENCES batches(id)
);
```

Database lookups return plain `dict` rows, never `Student` objects. That keeps the database layer independent of OOP. Conversion to `Student` happens in the GUI and web code.

### 6.4 Data file formats

| File | Format |
|---|---|
| `activity.txt` | one line per event: `2026-10-17 14:32:05 | Added student 111` |
| `export.csv` / `sample_students.csv` | header `roll,name,marks`, one row per student |
| `results.json` | list of `{"roll", "name", "marks", "grade"}` |
| `config.json` | `{"school": "Universal Ai University", "year": "2026-27"}` |
| `backup.pkl` | pickled list of row dicts (same shape as database rows) |
| `app.log` | `2026-10-17 14:32:05,123 INFO add_student called` |

### 6.4b Socket protocol (text, one message per line, ends with `\n`)

Fields are separated by `|` because names contain spaces.

| Client sends | Server replies |
|---|---|
| `RESULT 101` | `OK|101|Aarav Sharma|78.0|Pass` |
| `RESULT 999` | `ERROR|Student 999 not found` |
| `COUNT` | `OK|10` |
| `QUIT` | `OK|bye` (then closes the connection) |
| anything else | `ERROR|Unknown command` |

### 6.5 REST API

| Method and URL | Body | Success | Failure |
|---|---|---|---|
| `GET /api/students` | none | `200` list of student objects | none |
| `GET /api/students/<roll>` | none | `200` one student | `404 {"error": "..."}` |
| `POST /api/students` | JSON `{"roll", "name", "marks"}` | `201` created student | `400 {"error": "..."}` (bad marks, duplicate roll) |

Each student object in a reply is `{"roll", "name", "marks", "grade"}`.

### 6.6 Web routes

| Route | Method | Purpose | Template |
|---|---|---|---|
| `/` | GET | table of all students, fails highlighted | `index.html` |
| `/student/<int:roll>` | GET | one student's detail, `404` if missing | `student.html` |
| `/add` | GET, POST | form to add a student; POST saves, then redirects to `/` | `add.html` |

All templates extend `base.html` (shared header showing the school name from `config.json`).

### 6.7 GUI layout (Tkinter)

```
+------------------------------------------------------+
|  Roll [______]   Name [____________]   Marks [____]  |   <- grid()
|  [Add] [Update] [Delete] [Clear]       Search [____] |   <- grid()
+------------------------------------------------------+
|  Roll | Name              | Marks | Grade            |   <- ttk.Treeview
|  101  | Aarav Sharma      | 78    | Pass             |      + scrollbar
|  ...                                                 |
+------------------------------------------------------+
|  Status: ready                                       |   <- Label
+------------------------------------------------------+
```

Frames are stacked with `pack()`. Widgets inside the form frame use `grid()`.

**Events bound:**

| Event | Result |
|---|---|
| Button click | Add, Update, Delete, Clear |
| `<Return>` in the Marks entry | same as Add |
| `<Double-1>` on a table row | copy that row into the form fields |
| `<KeyRelease>` in Search | filter the table as you type |

---

## 7. Syllabus coverage map

Every topic from the syllabus, where it lives, and one sentence you can say about it.

### Module 1: Object-Oriented Programming in Python (CO1)

| Topic | Where | Say this |
|---|---|---|
| Classes and objects | `student.py`: `Student`, `Student(101, "Aarav", 78)` | A class is the blueprint, an object is one student made from it. |
| Constructors and destructors | `person.py`: `__init__`, `__del__` | `__init__` runs when the object is created; `__del__` runs when the last reference is gone (try `del s`), but Python does not promise exactly when. |
| Instance and class variables | `self.roll` vs `Student.PASS_MARK`, `Student.count` | Instance variables belong to one object; class variables are shared by all. |
| Methods in Python | `grade()` (instance), `from_csv_row()` (`@classmethod`), `valid_roll()` (`@staticmethod`) | Instance methods get `self`, class methods get `cls`, static methods get neither. |
| Encapsulation and data hiding | `self.__marks` with `get_marks()` / `set_marks()` | The double underscore makes Python rename it to `_Student__marks`, so outside code cannot change it by accident. It is a guard, not real security. |
| Inheritance and its types | `special.py` (see table below) | A child class reuses and extends its parent's code. |
| Polymorphism | `show_details()` overridden in every class | Same method name, different behaviour depending on the object. |
| Abstraction and abstract classes | `Person` with `@abstractmethod show_details` | You cannot create a plain `Person`; every subclass must implement `show_details`. |
| Operator overloading | `Student.__lt__`, `__add__`, `__str__` | `s1 < s2` quietly calls `s1.__lt__(s2)`. |

**Inheritance types (all in `special.py`):**

| Type | Example |
|---|---|
| Single | `Student(Person)` |
| Multilevel | `Person` → `Student` → `PGStudent` |
| Hierarchical | `Student` and `Teacher` both inherit from `Person` |
| Multiple | `TeachingAssistant(Student, Teacher)` |
| Hybrid | `TeachingAssistant` forms a diamond: `Person` → (`Student`, `Teacher`) → `TeachingAssistant` |

### Module 2: Advanced Functions and Functional Programming (CO2)

| Topic | Where | Say this |
|---|---|---|
| Scope and lifetime of variables | `scope_demo.py`: global `session_count`, locals, closure | A local variable dies when its function returns. `global` and `nonlocal` let a function change a variable outside itself. |
| Recursive functions | `functional_tools.py`: `total_marks(node)` | A function that calls itself on a smaller piece, with a stopping case. |
| Lambda functions | `sorted(students, key=lambda s: s.name)` | A tiny unnamed function written inline. |
| Higher-order functions | `apply_to_all(items, func)` | A function that takes another function as input (or returns one). |
| `map()`, `filter()`, `reduce()` | `add_grace()`, `failed_students()`, `class_total()` | `map` changes every item, `filter` keeps some, `reduce` folds everything into one value. |
| Iterators | `iterators_gens.py`: `Classroom` with `__iter__` / `__next__` | An iterator hands out one item at a time and raises `StopIteration` at the end. |
| Generators and `yield` | `student_rows()` | A function that pauses at `yield` and resumes later, producing values one at a time without loading everything. |
| Decorators | `decorators.py`: `@log_action`, `@timer`, `@admin_only` | A decorator wraps a function to add behaviour without editing the function. |
| Context managers | `context_meta.py`: `DBConnection` | `with` guarantees cleanup (commit or rollback, then close) even if an error happens inside. |
| Metaclasses | `context_meta.py`: `RegistryMeta` | A metaclass is the class of a class. Ours records every class the moment it is defined. |
| Dynamic typing | `scope_demo.py`: `normalise_roll()` | Variables have no type, values do. The same name can hold an int, then a string. |
| Modules and packages | the folder layout, `__init__.py`, `__name__ == "__main__"` | A module is one `.py` file, a package is a folder of modules. |

### Module 3: File Handling, Exception Handling and Database Connectivity (CO3)

| Topic | Where | Say this |
|---|---|---|
| Text file handling | `files.py`: `write_activity()`, `read_activity()` | Text files store readable characters; mode `"a"` appends, `"r"` reads. |
| Binary file handling | `files.py`: `backup_pickle()`, `restore_pickle()` (`"wb"` / `"rb"`) | Binary files store raw bytes; pickle turns Python objects into bytes and back. |
| CSV processing | `files.py`: `export_csv()`, `import_csv()` | The `csv` module reads and writes rows; `DictReader` gives one dict per row. |
| JSON processing | `files.py`: `save_json()`, `load_json()`, `load_config()` | JSON is a text format for dicts and lists that works across languages. |
| try / except / finally | `read_activity()`, database functions | `try` runs risky code, `except` handles the failure, `finally` always runs (for cleanup). |
| User-defined exceptions | `exceptions.py` | A subclass of `Exception` with a meaningful name. |
| Assertions | `exceptions.py`: `check_marks()` | `assert` is a developer self-check that `python -O` switches off. For user input, raise an exception instead. |
| Logging | `logger.py`, `data/app.log` | Logging writes timestamped, levelled messages to a file, which is better than `print`. |
| SQLite connectivity | `database.py` via `DBConnection` | SQLite is a full database in one file, built into Python. |
| CRUD operations | `add_student`, `get_student`, `update_marks`, `delete_student` | Create, Read, Update, Delete map to INSERT, SELECT, UPDATE, DELETE. |
| Introduction to MySQL | `mysql_demo.py` | Same idea as SQLite, but a separate server you log in to. |

### Module 4: Multithreading, Networking and API Programming (CO4)

| Topic | Where | Say this |
|---|---|---|
| Processes and threads | `threads.py`: `Thread` for backup, `Process` for report | Threads share memory inside one program; processes are separate programs with separate memory. |
| Multithreading in Python | `auto_backup` on a daemon thread | Background work without freezing the main program. In standard CPython the GIL means threads suit waiting work (I/O); processes suit heavy computation. |
| Thread synchronization | `Lock` in the counter demo, `with lock:` | A lock lets one thread at a time into a critical section, so updates are not lost. |
| Socket programming | `server.py`, `client.py` | A socket is one end of a network conversation; we use TCP. |
| Client-server communication | `RESULT 101` protocol, thread per client | The server waits and answers; the client connects and asks. |
| REST API basics | `web.py`: `/api/students` | A URL names a resource, an HTTP verb says the action, the reply is JSON, the status code says what happened. |
| Working with APIs using `requests` | `web_tools.py`: `fetch_students_from_api()` | `requests.get(url)` sends the request and `.json()` converts the reply. |
| JSON data parsing | same function | JSON becomes a Python list of dicts that you loop over. |
| Email automation | `web_tools.py`: `send_email()` | SMTP is the protocol for sending mail; we build a message and hand it to the mail server. |
| Web scraping using BeautifulSoup | `web_tools.py`: `scrape_books()` | Download the HTML, parse it into a tree, then pick elements by tag and class. |

### Module 5: GUI Programming and Web Frameworks (CO5)

| Topic | Where | Say this |
|---|---|---|
| GUI programming using Tkinter | `gui.py` | Tkinter is Python's built-in GUI toolkit; `mainloop()` waits for user events. |
| Event handling and widgets | `Button(command=...)`, `bind("<Return>")`, `<Double-1>`; `Label`, `Entry`, `Button`, `Treeview`, `messagebox` | An event is something the user does; a handler is the function we attach to it. |
| Layout management | `grid()` in the form, `pack()` for frames | `grid` uses rows and columns, `pack` stacks widgets, `place` uses exact coordinates (not used here). |
| Introduction to Flask | `web.py` | Flask is a small web framework where a Python function becomes a page. |
| Routing and templates | `@app.route`, Jinja templates, `base.html` | A route maps a URL to a function; a template is HTML with placeholders the function fills in. |
| Form handling | `/add` (GET shows form, POST saves) | GET fetches the form, POST submits it; after saving we redirect so a refresh does not resubmit. |
| Simple web application development | the results portal (`/`, `/student/<roll>`, `/add`) | A small app made of routes, templates, and the shared database layer. |
| Deployment basics | section 15 | Move from the dev server to a production setup with `debug` off and a proper server. |

---

## 8. File-by-file specification

### Module 1: `m1_oop/`

**`person.py`**
- `class Person(metaclass=RegistryMeta)` with an abstract `show_details()`.
  - `RegistryMeta` derives from `ABCMeta`, so abstract methods still work.
- Class variable `verbose = False`. `__del__` prints `"record closed for <name>"` only when `Person.verbose` is `True`. This keeps the GUI and Flask consoles quiet.
- `__init__(self, name)` stores `self.name`.
- `demo()`:
  1. Try `Person("x")` and catch `TypeError` (abstract class).
  2. Define a tiny inline subclass, set `Person.verbose = True`, create an object, then `del obj` to show the destructor.

**`student.py`**
- `class Student(Person)`:
  - class variables `PASS_MARK = 40  # CHANGE ME`, `count = 0`
  - `__init__(self, roll, name, marks)`: calls `super().__init__(name)`, sets `self.roll`, `self.__marks` via `set_marks`, increments `Student.count`
  - `get_marks()`, `set_marks(value)`: raises `InvalidMarksError` if not `0 <= value <= 100`
  - `grade()`: returns `"Pass"` or `"Fail"` using `Student.PASS_MARK`
  - `to_dict()`: returns `{"roll", "name", "marks", "grade"}`
  - `show_details()`, `__str__()`
  - `__lt__(self, other)`: compares marks. `__add__(self, other)`: returns the sum of both students' marks (an int)
  - `@classmethod from_csv_row(cls, row)`: builds a Student from a CSV dict row
  - `@staticmethod valid_roll(roll)`: `True` if it is a positive whole number
- `demo()`: create 3 students and show `Student.count`; compare a class variable with an instance variable; try `s.__marks` (AttributeError) then `s._Student__marks` (works, to explain name mangling); call `from_csv_row` and `valid_roll`.

**`special.py`**
- `Teacher(Person)`: `__init__(self, name, subject="General")`. The default matters: it lets `super()` work correctly in multiple inheritance.
- `PGStudent(Student)`: adds `thesis`. Multilevel.
- `TeachingAssistant(Student, Teacher)`: `__init__(self, roll, name, marks, subject)` calls `Student.__init__(...)` then sets `self.subject`.
- Each class overrides `show_details()`.
- `demo()`: put one object of each type in a list and loop `for p in people: p.show_details()` (polymorphism); print `TeachingAssistant.__mro__` and explain the diamond.

**`operators.py`** (demo only; the operator methods live in `Student`)
- `demo()`: `sorted(students)` uses `__lt__`, `max(students)`, and `s1 + s2` uses `__add__`.

### Module 2: `m2_functional/`

**`functional_tools.py`**
- `apply_to_all(items, func)`: returns `[func(i) for i in items]` using a plain loop (higher-order).
- `add_grace(students)`: `map` with `lambda`, `+5` marks capped at 100. `# CHANGE ME: grace marks`
- `failed_students(students)`: `filter` with a `lambda` on `grade() == "Fail"`.
- `class_total(students)`: `reduce(lambda total, s: total + s.get_marks(), students, 0)`.
- `sort_students(students, key)`: wraps `sorted(students, key=key)`.
- `total_marks(node)`: recursive. If `node` is a list, sum its students' marks; if a dict, add up `total_marks` of each value.
- `demo()`: builds `{"AIML": {"Sem3-A": [101..103], "Sem3-B": [104..106]}, "DS": {"Sem3-A": [107..110]}}` and checks `total_marks` equals 569.

**`iterators_gens.py`**
- `class Classroom`: holds a list; `__iter__` returns itself; `__next__` returns the next student or raises `StopIteration`.
- `student_rows()`: generator. Opens `DBConnection`, loops over `SELECT roll, name, marks FROM students`, and `yield`s one row at a time.
- `demo()`: loop over a `Classroom` with `for`; call `next()` by hand until `StopIteration`; print the first 3 rows from `student_rows()`.
- Note: a generator keeps its DB connection open until it finishes, so consume it fully.

**`decorators.py`**
- `CURRENT_ROLE = "admin"  # CHANGE ME`
- `log_action(func)`: logs the function name via the `srm` logger. Use `functools.wraps`.
- `timer(func)`: prints how long the call took.
- `admin_only(func)`: raises `PermissionError` unless `CURRENT_ROLE == "admin"`.
- `demo()`: decorate three small functions and call them; change `CURRENT_ROLE` to `"guest"` to show the block.

**`context_meta.py`**
- `class DBConnection`: `__init__(self, db_name=settings.DB_NAME)`. `__enter__` opens `sqlite3.connect` with `row_factory = sqlite3.Row` and returns it. `__exit__` commits if no error, rolls back if there was one, always closes, and returns `False` so errors still propagate.
- `class RegistryMeta(ABCMeta)`: class-level `registry = {}`; `__init__(cls, name, bases, namespace)` calls `super().__init__(...)` then `RegistryMeta.registry[name] = cls`.
- `demo()`: use `with DBConnection() as conn:`; print `RegistryMeta.registry` keys (expect `Person`, `Student`, `Teacher`, `PGStudent`, `TeachingAssistant` once `m1_oop` is imported inside `demo()`).

**`scope_demo.py`**
- `session_count = 0` (global). `open_session()` uses `global` to add 1.
- `make_counter()`: closure; inner function uses `nonlocal`.
- `normalise_roll(value)`: accepts `101`, `"101"`, `"101 "`, or `101.0` and returns `int`. Raises `ValueError` otherwise.
- `demo()`: show a local variable gone after return; show `x = 5` then `x = "five"` and print `type(x)` each time; call `normalise_roll` with several types.

### Module 3: `m3_data/`

**`exceptions.py`**
- `class InvalidMarksError(Exception)` and `class StudentNotFoundError(Exception)` (docstring only, no body).
- `check_marks(marks)`: `assert 0 <= marks <= 100, "marks out of range"`.
- `demo()`: trigger each, catch with `try/except/finally`, and explain: assertions are for programmer mistakes, exceptions are for bad user input.

**`logger.py`**
- `setup_logging()`: `logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")`.
- `demo()`: log one INFO, one WARNING, and one ERROR line, then print the last 3 lines of `app.log`.

**`files.py`**
- Text: `write_activity(text)` (append with timestamp), `read_activity()` (one function uses an explicit `open` / `try` / `except FileNotFoundError` / `finally: f.close()` to show `finally`).
- CSV: `export_csv(rows)` with `csv.DictWriter`; `import_csv()` with `csv.DictReader`.
- JSON: `save_json(rows)`, `load_json()`, `load_config()`.
- Binary: `backup_pickle(rows)` (`"wb"`), `restore_pickle()` (`"rb"`). Only load pickle files you created yourself.
- `demo()`: write two log lines and read them back; export then re-import CSV; save and reload JSON; pickle backup then restore and compare to the original.
- `# ADD FIELD HERE` on the CSV header list and row dict.

**`database.py`**
- `create_table()`, `seed_from_csv()` (only if the table is empty).
- `add_student(roll, name, marks)` (`@log_action`), `get_student(roll)` (raises `StudentNotFoundError`), `get_all_students()`, `search_students(text)` (`LIKE ?`), `update_marks(roll, marks)` (`@log_action`), `delete_student(roll)` (`@log_action`, `@admin_only`).
- Each function uses `with DBConnection() as conn:` and returns `dict` rows.
- Duplicate roll raises `sqlite3.IntegrityError`. The GUI and web layers catch it and show "Roll already exists".
- `# ADD FIELD HERE` on the `CREATE TABLE`, the `INSERT`, and the row-to-dict conversion.
- `demo()` / `__main__`: create the table, seed it, then run one of each CRUD operation and print the result.

**`mysql_demo.py`**
- Reads `settings.MYSQL`. Imports `mysql.connector` inside `demo()` inside `try`, so a missing package prints "MySQL package not installed, skipping" instead of crashing.
- Connects, creates the `students` table if missing, runs `SELECT`, prints rows. Catch `mysql.connector.Error` and print "MySQL server not reachable, skipping".

### Module 4: `m4_network/`

**`threads.py`**
- `auto_backup(stop_event)`: loop. Each pass exports the DB to `BACKUP_FILE` via `backup_pickle`, then `stop_event.wait(settings.BACKUP_INTERVAL)`.
- `run_counter_demo(use_lock)`: two threads each add 100000 to a shared counter, with or without `with lock:`. To make the race visible, add `time.sleep(0)` between reading and writing the counter.
- `build_report()`: writes count, average, highest, and pass percentage to `REPORT_FILE`. Run it in a `multiprocessing.Process`.
- `demo()`:
  1. start `auto_backup` as a `daemon=True` thread, then stop it with the event
  2. run the counter demo twice (no lock, then lock)
  3. start and `join()` the report process
- The Process code **must** sit under `if __name__ == "__main__":` (required on Windows).

**`server.py`**
- `handle_command(line)`: a pure function that takes one request line and returns the reply string, following section 6.4b. Easy to test and easy to extend with `elif`.
- `handle_client(conn, addr)`: loop `recv(1024)` → `handle_command` → `sendall`; stop on `QUIT` or empty data; always close the connection in `finally`.
- `start_server()`: `socket.socket(AF_INET, SOCK_STREAM)`, `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)`, `bind((HOST, SOCKET_PORT))`, `listen()`, then loop on `accept()` and start `threading.Thread(target=handle_client, args=(conn, addr), daemon=True)` for each client.
- `demo()` calls `start_server()` (blocks; run it in its own terminal).

**`client.py`**
- `send_command(text)`: connect, send, receive, return the reply. Catch `ConnectionRefusedError` and return `"ERROR|Server is not running"`.
- `demo()`: loop on `input()` until the user types `quit`.

**`web_tools.py`**
- `fetch_students_from_api()`: `requests.get(f"http://{HOST}:{FLASK_PORT}/api/students", timeout=5)`, `response.json()`, then print each student. Catch `requests.exceptions.RequestException` and print "Start the web app first".
- `scrape_books(limit=5)`: get `BOOKS_URL`, set `response.encoding = "utf-8"` (otherwise prices show as `Â£`), `BeautifulSoup(response.text, "html.parser")`, loop over `article.product_pod`, print `h3 a["title"]` and `p.price_color`. `# CHANGE ME: limit`
- `send_email(subject, body)`: build an `EmailMessage`. If `EMAIL_TEST_MODE` print it. Otherwise `smtplib.SMTP(SMTP_HOST, SMTP_PORT)` → `starttls()` → `login(EMAIL_FROM, os.environ["SRM_EMAIL_PASSWORD"])` → `send_message`.
- `demo()`: runs all three; the email body is built from the first student's result.

### Module 5: `m5_apps/`

**`gui.py`**
- `class App`: `__init__(self, root)`, `build_form()`, `build_table()`, `refresh()`, `clear_form()`, `on_add()`, `on_update()`, `on_delete()`, `on_select(event)`, `on_search(event)`.
- `ttk.Treeview(columns=("roll", "name", "marks", "grade"), show="headings")` with a scrollbar. Rows are inserted with `tree.insert("", "end", values=(...))`.
- Values read back from the Treeview can come back as strings, so pass the roll through `normalise_roll()` (ties to dynamic typing).
- Handlers catch `InvalidMarksError`, `StudentNotFoundError`, `sqlite3.IntegrityError`, and `ValueError`, and show a `messagebox` plus a status-bar message.
- `# ADD FIELD HERE` on the form `Entry`, the Treeview columns, and the add/update handlers.
- `main()`: `setup_logging()`, `create_table()`, create the root window, `mainloop()`.
- If you add a "Backup now" button that uses a thread, update the GUI from that thread only through `root.after(...)`. Tkinter is not thread-safe.

**`web.py`**
- `app = Flask(__name__)`.
- Routes from section 6.6 and the REST API from section 6.5. API routes use `jsonify` and `request.get_json()`; web pages use `render_template`, `request.form`, `redirect(url_for("index"))`, and `abort(404)`.
- Convert the form roll with `normalise_roll()` inside `try`; show errors on the form page.
- `# ADD FIELD HERE` on the form handler and in `add.html`.
- Run only under `if __name__ == "__main__": app.run(host=HOST, port=FLASK_PORT, debug=True)`. The server is loopback-only and ignores `PORT`. Debug mode starts the code twice (the reloader), so never start threads at import time.

**Templates**
- `base.html`: `<title>`, header with school name, `{% block content %}{% endblock %}`.
- `index.html`: `{% extends "base.html" %}`, `{% for s in students %}`, `{% if s.grade == "Fail" %}` adds a red row class.
- `student.html`: name, roll, marks, grade, and a back link using `url_for`.
- `add.html`: a form with `method="post"` and `action="{{ url_for('add_student') }}"`, plus an error message block.

---

## 9. `main.py` menu

Each entry is a module path. `main.py` imports it lazily with `importlib.import_module(path).demo()`.

```python
MENU = {
    "1":  ("Constructor, destructor, abstract class", "m1_oop.person"),
    "2":  ("Class vs instance vars, encapsulation, methods", "m1_oop.student"),
    "3":  ("Inheritance types and polymorphism", "m1_oop.special"),
    "4":  ("Operator overloading", "m1_oop.operators"),
    "5":  ("lambda, map, filter, reduce, recursion", "m2_functional.functional_tools"),
    "6":  ("Iterators and generators", "m2_functional.iterators_gens"),
    "7":  ("Decorators", "m2_functional.decorators"),
    "8":  ("Context manager and metaclass", "m2_functional.context_meta"),
    "9":  ("Scope and dynamic typing", "m2_functional.scope_demo"),
    "10": ("Text, CSV, JSON, binary files", "m3_data.files"),
    "11": ("Exceptions and assertions", "m3_data.exceptions"),
    "12": ("SQLite CRUD", "m3_data.database"),
    "13": ("MySQL intro", "m3_data.mysql_demo"),
    "14": ("Threads, lock, process", "m4_network.threads"),
    "15": ("Socket server (blocks, use its own terminal)", "m4_network.server"),
    "16": ("Socket client", "m4_network.client"),
    "17": ("requests, scraping, email", "m4_network.web_tools"),
    "18": ("Tkinter app", "m5_apps.gui"),
    "19": ("Flask app", "m5_apps.web"),
}
```

- `0` exits. Invalid input prints "Choose a number from the list".
- `main.py` calls `setup_logging()` once at start.
- Adding a menu item live is one new line in `MENU`.

---

## 10. Verification checkpoints

Run these after finishing each module. If the output matches, the module is done.

| Module | Command | Expected |
|---|---|---|
| 1 | `python -m m1_oop.person` | `TypeError` caught for `Person("x")`; "record closed for ..." printed after `del`. |
| 1 | `python -m m1_oop.student` | `Student.count` goes up with each new student; `s.__marks` fails, `s._Student__marks` works. |
| 1 | `python -m m1_oop.special` | Each object prints its own `show_details()`; the MRO shows `TeachingAssistant → Student → Teacher → Person`. |
| 2 | `python -m m2_functional.functional_tools` | Total 569; grace total 619; 3 failed students; recursive total also 569. |
| 2 | `python -m m2_functional.decorators` | Log lines in `app.log`; time printed; guest role raises `PermissionError`. |
| 2 | `python -m m2_functional.context_meta` | Registry lists all 5 person classes. |
| 3 | `python -m m3_data.database` | Table created, 10 rows seeded, CRUD results printed. Running it twice does not duplicate rows. |
| 3 | `python -m m3_data.files` | Activity lines read back; CSV re-import matches; pickle restore equals the original list. |
| 4 | `python -m m4_network.threads` | Without the lock the counter is often below 200000 (if it is not, add the `sleep(0)`); with the lock it is exactly 200000. |
| 4 | server + client | `RESULT 101` returns `OK|101|Aarav Sharma|78.0|Pass`; two clients at once both work. |
| 4 | `python -m m4_network.web_tools` | 5 book titles and prices; email printed in test mode; API call works while Flask runs. |
| 5 | `python -m m5_apps.gui` | 10 rows appear; add, update, delete work and the table refreshes. |
| 5 | `python -m m5_apps.web` | `/` shows 10 rows with fails in red; `/add` saves; `/api/students` returns JSON. |

**Cross-check (best proof of the shared database):** add a student in the Tkinter window, refresh the Flask page, and see them there. Then ask the socket server for that roll.

---

## 11. Live-change cheat sheet

| Professor says | File | What to change |
|---|---|---|
| "Change the pass mark to 50" | `m1_oop/student.py` | `PASS_MARK = 50`. Check: 5 fails. |
| "Add A/B/C grades" | `m1_oop/student.py`, `grade()` | `if m >= 75: return "A"` / `elif m >= 60: return "B"` / `elif m >= PASS_MARK: return "C"` / `else: return "Fail"`. Check: A=3, B=1, C=3, Fail=3. Also fix `failed_students()` if it compares with `"Pass"`. |
| "Add another type of student" | `m1_oop/special.py` | Copy `PGStudent`, rename it, change the extra field and `show_details()`. |
| "Sort by name" / "highest first" | `functional_tools.py` | `key=lambda s: s.name`, or add `reverse=True`. |
| "Show only failed students" | `functional_tools.py`, `failed_students()` | Change the `filter` condition. |
| "Give 10 grace marks" | `functional_tools.py`, `add_grace()` | `5` → `10`. |
| "Write a new decorator" | `decorators.py` | Copy `log_action`, change the message. Apply with `@name` above a function. |
| "Show the decorator blocking something" | `decorators.py` | `CURRENT_ROLE = "guest"`, then delete a student. |
| "Add a new exception" | `m3_data/exceptions.py` | `class DuplicateRollError(Exception): pass` and `raise` it. |
| "Add an email field" | search `ADD FIELD HERE` | About 6 places: `Student.__init__`, `database.py` (CREATE TABLE, INSERT, row-to-dict), `files.py` (CSV header and row), `gui.py` (Entry), `web.py` and `add.html`. Delete `data/students.db` and re-seed. **Rehearse this one.** |
| "Add a CSV column" | `m3_data/files.py` | The header list and the row dict. |
| "Change the server port" | `settings.py` | `SOCKET_PORT = 6000` (server and client both read it). |
| "Add a new server command" | `m4_network/server.py`, `handle_command()` | New `elif line.startswith("TOP"):` branch returning `OK|...`. |
| "Change the backup interval" | `settings.py` | `BACKUP_INTERVAL = 10`. |
| "Scrape more books" | `m4_network/web_tools.py` | `limit=5` → `limit=10`. |
| "Really send the email" | `settings.py` | `EMAIL_TEST_MODE = False`, set `SRM_EMAIL_PASSWORD` (Gmail needs an app password). |
| "Add a button" | `m5_apps/gui.py` | 3 lines: write `on_xxx()`, create `Button(command=self.on_xxx)`, call `.grid(...)`. |
| "Add a web page" | `m5_apps/web.py` + `templates/` | A 4-line `@app.route` function and a small template extending `base.html`. |
| "Add a new REST endpoint" | `m5_apps/web.py` | Copy `api_one`, change the route and the query. |
| "Add a menu item" | `main.py` | One new line in `MENU`. |

---

## 12. Break-it-on-purpose tests

Do these live to show error handling working.

| Do this | What should happen |
|---|---|
| Enter marks `150` in the GUI | `InvalidMarksError` caught, `messagebox` appears, ERROR line in `app.log`. |
| Add a student with an existing roll | "Roll already exists", no crash. |
| Ask for roll `999` (GUI search, web, or socket) | `StudentNotFoundError`, friendly message, `404` on the web. |
| `Person("x")` | `TypeError`: abstract class cannot be instantiated. |
| Run the client with the server stopped | "Server is not running". |
| Run `fetch_students_from_api()` with Flask stopped | "Start the web app first". |
| Run `python -O -m m3_data.exceptions` | The `assert` is skipped. This shows why asserts are not for user input. |
| Remove the `with lock:` line | The counter total is wrong. |
| Set `CURRENT_ROLE = "guest"` | Delete raises `PermissionError`. |
| Enter `abc` as the roll in the web form | Error shown on the form, no crash. |

---

## 13. Likely follow-up questions

| Question | Short answer |
|---|---|
| Why is `__del__` unreliable? | Python calls it when the object is garbage collected, not at a guaranteed moment, and not reliably at interpreter exit. Use a context manager for cleanup that must happen. |
| Is `__marks` really private? | No. Python renames it to `_Student__marks`. It prevents accidents, not determined access. |
| What if a subclass skips an abstract method? | Creating an object of that subclass raises `TypeError`. |
| Iterator vs generator? | A generator is a shortcut for writing an iterator: `yield` replaces the manual `__iter__` / `__next__` and state tracking. |
| Why `functools.wraps` in a decorator? | It keeps the original function's name and docstring, otherwise every decorated function would be called `wrapper`. |
| Why `with` for the database? | It guarantees commit-or-rollback and close, even when an error happens. |
| Why `?` placeholders in SQL? | They prevent SQL injection, because the value is never treated as SQL code. |
| Thread vs process? | Threads share memory and are cheap; processes are isolated with their own memory. Because of the GIL, CPU-heavy work uses processes. |
| Why a lock? | Two threads can read the same value, both add 1, and both write back, losing one update. The lock forces them to take turns. |
| Why one thread per client in the server? | Otherwise one slow client would block everyone else. |
| GET vs POST? | GET reads and is safe to repeat; POST sends data to change something. |
| Why redirect after POST? | So that refreshing the page does not submit the form again. |
| Why not deploy with `app.run`? | It is a development server. Production uses a WSGI server such as gunicorn or waitress, with `debug` off. |
| Why `after()` in Tkinter? | Tkinter is not thread-safe; background threads must ask the main thread to update widgets. |

---

## 14. Demo script (about 8 minutes)

1. **Show the folder tree** (30 s): one folder per syllabus module.
2. **`python main.py`** and run a few menu items per module (3 min):
   - Module 1: item 3 (inheritance and polymorphism)
   - Module 2: items 5, 7, 8
   - Module 3: items 10, 12
3. **Network** (1.5 min): terminal 1 runs the server (item 15), terminal 2 the client (`RESULT 101`), then item 17.
4. **GUI to web** (2 min): add a student in Tkinter, refresh the Flask page, and open `/api/students`.
5. **Close with a live change** (1 min): change `PASS_MARK` to 50, re-run, and show 5 fails.

Keep section 11 and section 12 open in a second window.

---

## 15. Deployment note (Module 5: deployment basics)

1. **Freeze dependencies:** `pip freeze > requirements.txt`.
2. **Development vs production:** Flask's built-in server (`app.run`) is for development only. For production set `debug=False` and use a WSGI server: `gunicorn` on Linux or `waitress` on Windows (`waitress-serve --port=8000 m5_apps.web:app`).
3. **Configuration:** secrets such as the email password come from environment variables, never from the code.
4. **PythonAnywhere (free hosting for a demo):**
   - upload the project and create a virtualenv
   - `pip install -r requirements.txt`
   - on the Web tab set the WSGI file to `from m5_apps.web import app as application`
   - click Reload
   - free accounts limit outgoing internet access, so scraping and email may not work there
5. **What is deployed:** only the Flask app. Tkinter and the socket server are local programs.
6. **SQLite** is fine for a demo; a busy production site would use MySQL or PostgreSQL.

---

## 16. Build order and definition of done

### Two-week plan

| Days | Work |
|---|---|
| 1 to 2 | `settings.py`, sample data, `exceptions.py`, `logger.py`, `context_meta.py`, then all of Module 1 |
| 3 to 4 | rest of Module 2 |
| 5 to 6 | Module 3 (`database.py` first, then `files.py`, `mysql_demo.py`) |
| 7 to 8 | Module 4 |
| 9 to 10 | Module 5 |
| 11 to 12 | `main.py`, cross-checks, rehearse section 11 |
| 13 to 14 | Mock viva with a friend using sections 11, 12, and 13 |

### A file is done when

- [ ] it runs with `python -m package.file` and `demo()` prints something clear
- [ ] it has the 2-line docstring, a `# CHANGE ME:` block where relevant, and `# CONCEPT:` tags
- [ ] it respects the layer rule (section 5)
- [ ] it stays within about 60 lines (GUI and web about 90)
- [ ] you can explain every line without looking at notes
- [ ] its checkpoint in section 10 passes

### Progress tracker

- [ ] Foundation: `settings.py`, `data/` files, `exceptions.py`, `logger.py`, `context_meta.py`
- [ ] Module 1: `person.py`, `student.py`, `special.py`, `operators.py`
- [ ] Module 2: `functional_tools.py`, `iterators_gens.py`, `decorators.py`, `scope_demo.py`
- [ ] Module 3: `files.py`, `database.py`, `mysql_demo.py`
- [ ] Module 4: `threads.py`, `server.py`, `client.py`, `web_tools.py`
- [ ] Module 5: `gui.py`, `web.py`, 4 templates
- [ ] `main.py` and the cross-check from section 10
- [ ] Section 11 rehearsed (especially "add a field")

---

## 17. Prompts to use with an AI assistant

Paste this whole file first, then use one prompt at a time.

**Build a module:**
> Using context.md, write every file in `m1_oop/` exactly as specified in sections 2, 5, 7, and 8. Follow the coding rules. Give one file at a time, with plain-English comments and the `# CONCEPT:` tags.

**Explain a file:**
> Explain `m2_functional/decorators.py` line by line as if I must teach it to my professor. Give me one sentence per concept from the section 7 table, then 3 likely follow-up questions.

**Practise live changes:**
> Act as my professor. Pick 5 random items from the section 11 cheat sheet, ask me one at a time, and tell me which file I should open and what I should change after I answer.

---

## 18. Known pitfalls

| Pitfall | Fix |
|---|---|
| `ModuleNotFoundError` | Run from the project root with `python -m package.file`. |
| Relative paths fail | Always run from `student_manager/`. |
| `OSError: Address already in use` | A previous server is still running. `SO_REUSEADDR` helps; otherwise change `SOCKET_PORT`. |
| Windows firewall popup on first server run | Allow access on private networks. |
| `Process` runs the whole script again on Windows | Keep process code under `if __name__ == "__main__":`. |
| Tkinter freezes or crashes from a thread | Touch widgets only from the main thread; use `root.after()`. |
| SQLite error about threads | Open a fresh connection per call (`DBConnection`) instead of sharing one across threads. |
| `database is locked` | Two programs wrote at the same instant; retry. Do not hold connections open (this is why generators must be consumed fully). |
| Flask code runs twice | The debug reloader does this. Never start threads at import time. |
| `Â£` instead of `£` when scraping | Set `response.encoding = "utf-8"` before reading `response.text`. |
| Destructor messages flood the console | Keep `Person.verbose = False` except in the demo. |
| Gmail login fails | Use an app password, not your normal password; keep `EMAIL_TEST_MODE = True` until the demo. |
| Unpickling a file you did not create | Never do this; pickle can run code. Only restore your own backups. |
| MySQL demo crashes | It should print a skip message; check the `try/except` around the import and the connection. |
