# Student Record Manager — delivery outcomes

## Foundation, project rules, and sample data
- [x] Provide Python 3.10+ setup instructions, requirements for Flask, requests, and beautifulsoup4, and optional `mysql-connector-python` only for the MySQL demo; document Tkinter platform availability and running from the project root with `python -m package.file`.
- [x] Create the specified package/folder structure, keep every `__init__.py` empty, keep imports within the layer rules, make `main.py` import modules lazily, and ensure each runnable module is independently runnable with `demo()` and `if __name__ == "__main__": demo()`.
- [x] Follow the source rules: readable plain code; no walrus operator, nested comprehensions, one-line tricks, or type hints; two-line module docstring; explain why in comments; keep functions at or below about 15 lines; put shared settings in `settings.py`, file-specific editable values in `# CHANGE ME:` blocks, and include `# CONCEPT:` and `# ADD FIELD HERE` markers at the documented locations. The approximate module-size target is observed where practical; a few full-feature modules remain longer to hold the required examples and interfaces.
- [x] Use parameterized SQL (`?` placeholders), friendly errors at user-facing boundaries, and technical logging. Do not add login/security hardening, async code, ORM, a test framework, or roles beyond the decorator demonstration.
- [x] Include the 10 specified CSV seed students (rolls 101–110 with their exact names and marks), and the config JSON for Universal Ai University, year 2026–27. Seed only when the database is empty.
- [x] Preserve expected sample facts: 10 students; total marks 569; average 56.9; highest 103 Rohan Mehta with 92; pass mark 40 has failures 102, 106, 110; pass mark 50 has failures 102, 105, 106, 109, 110; +5 capped grace marks total 619; the documented A/B/C/Fail boundaries yield A: 101, 103, 108; B: 107; C: 104, 105, 109; Fail: 102, 106, 110.

## Module 1 — object-oriented programming
- [x] Implement abstract `Person` with `RegistryMeta`, constructor/destructor behavior and `verbose=False`; its demo catches the abstract-class `TypeError`, then enables and demonstrates the destructor.
- [x] Implement `Student(Person)` with `PASS_MARK = 40`, `count`, encapsulated marks validated by `InvalidMarksError`, `grade()`, `to_dict()`, `show_details()`, `__str__`, `__lt__`, `__add__`, classmethod `from_csv_row()`, and staticmethod `valid_roll()`. Demonstrate class/instance variables, name mangling, CSV creation, and roll validation.
- [x] Implement `Teacher`, `PGStudent`, and `TeachingAssistant` to demonstrate single, multilevel, hierarchical, multiple, and hybrid inheritance; override `show_details()` and demonstrate polymorphism and the MRO.
- [x] Demonstrate operator overloading through `sorted(students)`, `max(students)`, and `s1 + s2`.

## Module 2 — advanced functions
- [x] Implement higher-order `apply_to_all`, lambda/map grace marks capped at 100, filter-based failed students, reduce-based class total, sorting by key, and recursive nested-list/dict mark totals. The demo’s department tree totals 569.
- [x] Implement the `Classroom` iterator with `__iter__`/`__next__`, plus a database-backed `student_rows()` generator that yields rows and documents that it must be consumed fully to close the connection.
- [x] Implement `@log_action` with `functools.wraps`, `@timer`, and `@admin_only`; demonstrate admin success and guest-role `PermissionError`.
- [x] Implement `DBConnection` as a context manager that commits or rolls back and always closes, plus `RegistryMeta(ABCMeta)` that registers classes; its demo shows the registry after importing the OOP types inside the demo.
- [x] Demonstrate global, local, and nonlocal scope, closure counter, dynamic typing, and `normalise_roll()` accepting integer/string/decimal forms such as `101`, `"101"`, `"101 "`, and `101.0`, while rejecting invalid values.

## Module 3 — files, exceptions, and database
- [x] Define `InvalidMarksError` and `StudentNotFoundError`; demonstrate `assert` bounds checks and `try/except/finally`, while explaining that assertions are not user-input validation.
- [x] Configure the `srm` logger to write timestamped INFO/WARNING/ERROR entries to `data/app.log` and show the latest three lines.
- [x] Implement activity text append/read with timestamps and an explicit `open`/`try`/`except FileNotFoundError`/`finally` close; CSV import/export; JSON save/load/config; and pickle backup/restore using only backups created by this program. Put `# ADD FIELD HERE` on the CSV header and row mapping.
- [x] Implement SQLite table creation and seed-if-empty; `add_student`, `get_student`, `get_all_students`, `search_students`, `update_marks`, and `delete_student`. Each uses `DBConnection`, returns plain row dictionaries, raises `StudentNotFoundError` when absent, logs decorated mutations, and marks `# ADD FIELD HERE` at schema, insert, and row mapping. Duplicate rolls raise `sqlite3.IntegrityError` for the UI to translate to “Roll already exists”.
- [x] Include an optional MySQL demo whose connector import occurs inside `demo()` and whose missing driver or unreachable server prints a skip message rather than crashing.

## Module 4 — threads, sockets, APIs, and utilities
- [x] Implement periodic pickle backup on a daemon thread controlled by a stop event; demonstrate a two-thread counter with and without `Lock`, yielding exactly 200000 with the lock; and build the report in a `multiprocessing.Process`, keeping process execution under the main guard for Windows.
- [x] Implement the TCP socket server with `SO_REUSEADDR`, the configured host/port, one daemon thread per client, newline-delimited messages, and always-close cleanup; create the table and seed the CSV on clean server startup. `RESULT 101` returns `OK|101|Aarav Sharma|78.0|Pass`; missing roll returns `ERROR|Student 999 not found`; `COUNT` returns `OK|10`; `QUIT` returns `OK|bye`; unknown commands return `ERROR|Unknown command`.
- [x] Implement a socket client that catches `ConnectionRefusedError` and returns `ERROR|Server is not running`, with an input loop ending on `quit`.
- [x] Implement `requests` API fetching with a five-second timeout, JSON parsing, a friendly “Start the web app first” message for connection errors; scrape the requested Books to Scrape site using BeautifulSoup and UTF-8 encoding; and email via `EmailMessage`, printing in test mode by default and reading any real SMTP password only from `SRM_EMAIL_PASSWORD`.

## Module 5 — desktop and web applications
- [x] Implement the Tkinter staff CRUD GUI with form fields, Add/Update/Delete/Clear, search-as-you-type, a `ttk.Treeview` with scrollbar, row selection into fields, Enter-to-add, status feedback, and friendly message boxes for invalid marks, missing students, duplicate rolls, and invalid input. Use `pack()` for stacked frames and `grid()` within the form; convert selected rolls with `normalise_roll()`; place `# ADD FIELD HERE` at the form, table columns, and handlers.
- [x] Implement Flask routes `/` (all students with failures visibly highlighted), `/student/<int:roll>` (detail or 404), and `/add` (GET form, POST save, then redirect); templates `base.html`, `index.html`, `student.html`, and `add.html` extend the shared base, show school name from config, handle form errors, and include the documented add-field marker.
- [x] Implement REST `GET /api/students` (200 list), `GET /api/students/<roll>` (200 single record or 404 `{"error":"..."}`), and `POST /api/students` (JSON `roll`, `name`, `marks`; 201 on success, 400 JSON error for invalid marks or duplicate roll). Each student response is `{"roll", "name", "marks", "grade"}`.
- [x] Make the web portal a polished, responsive academic dashboard with student/pass/average/highest summaries, searchable/filterable student list, grade/status labels, detail view, and accessible record-management workflows; include loading/empty/error/success states, keyboard focus and confirmation for destructive actions. Keep the server-rendered Flask/Jinja architecture and the supplied school/year identity.
- [x] Keep Flask startup fixed to loopback `127.0.0.1:5001` with debug enabled for local development; ignore `PORT`. Serve a complete `public/manus-routes.json` at `/manus-routes.json` for `/`, `/student/:roll`, and `/add`.

## Delivery and documented learning workflow
- [x] Include a README with setup, run commands for the menu, individual demos, database, socket server/client, Tkinter app, Flask app, API examples, common pitfalls, and production deployment notes (debug off, WSGI server, only Flask deployed; Tkinter/socket remain local).
- [x] Ensure all module demos are clear and the documented manual checkpoints work: database remains seeded once across repeated runs; files round-trip through CSV/JSON/pickle; counter lock gives 200000; API/web results match seed data; invalid inputs and missing rows produce friendly messages; and the shared SQLite layer is used by GUI, Flask, and socket server.
- [x] Preserve the live-change cheat sheet and viva topics in the supplied `context.md`, including pass-mark changes, A/B/C grades, adding a field, port/backup changes, decorators, API endpoints, and menu items.
