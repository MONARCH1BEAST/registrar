# Student Record Manager — Viva and Practical Guide

This guide describes the implementation found in the repository, not every intention in the older course specification. **Verified** means exercised during the 2026-10-20 audit; **Source-derived** means established by code inspection; **Proposed** means an examiner challenge that would add or change code. No formal test suite exists.

## 1. Project introduction and presentation

### 30-second introduction

> “Student Record Manager is a small Python teaching project organized around a student-and-marks example. It demonstrates five areas: object-oriented Python, functional programming, files and SQLite, networking and concurrency, and desktop/web applications. The Flask and Tkinter interfaces, as well as the TCP demonstration, use one SQLite CRUD layer. It is designed for learning and local demonstration, not as a secured production student-information system.”

### Two-minute technical explanation

> “The project is split into five packages. `m1_oop` defines `Person` and `Student`, including validation, grading, inheritance and operator overloading. `m2_functional` demonstrates higher-order functions, iterators, decorators, closures, a context manager and a metaclass. `m3_data` contains the SQLite CRUD module, custom exceptions, logging and CSV, JSON, text and pickle examples. `m4_network` contains a threaded TCP server/client, concurrency examples, an HTTP client, scraping and an email example. `m5_apps` has a Tkinter client and a Flask portal with HTML pages and a small JSON API.
>
> “The database is `data/students.db`; `settings.py` centralizes paths and ports. `m3_data.database` returns dictionaries, so the interfaces do not need to issue their own SQL. The Flask request hook creates the table and seeds CSV data only when it is empty. The web API currently supports listing, reading one record and creating; marks updates and deletion use the HTML detail form. The project is intentionally a coursework demonstration: it has no real authentication or CSRF defense, no migration tooling, and no automated test suite.”

### Five-minute demonstration plan

1. **Introduce the menu:** run `python main.py`; explain lazy `importlib` loading and select a short concept module.
2. **Show the domain rule:** run `python -m m1_oop.student` or inspect `Student.grade()` and `set_marks()`. State that marks 40 and above pass by default.
3. **Show functional processing:** run `python -m m2_functional.functional_tools`; point out the expected total 569, grace total 619 and three failures at pass mark 40.
4. **Show shared persistence:** run `python -m m3_data.database`, then launch `python -m m5_apps.web`. Demonstrate list and add; if possible, show that a row created in one interface appears in another.
5. **Show one API call:** use `Invoke-RestMethod http://localhost:5001/api/students`.
6. **Demonstrate deletion:** on a student detail page select Delete. Explain that Cancel, clicking outside the modal, or pressing Escape closes it without sending the delete POST; Delete record submits the existing `/student/<roll>` form. Keyboard focus stays within the modal and returns to the Delete button when canceled.
7. **Optionally show TCP:** run the server and client in separate terminals; submit `COUNT`, `RESULT 101`, and `QUIT`.
8. **Finish honestly:** explain that the GUI requires a desktop, the MySQL and SMTP options are not exercised, and the web app has no authentication and is only for local learning.

Avoid presenting a running sample database as a guaranteed clean state. If you need deterministic starting data, use a separately backed-up demo database; the project’s seed function inserts only when the table is empty.

### Problem, objectives, choices and limitations

- **Problem:** give Python concepts one consistent, familiar data domain.
- **Objective:** make the same basic student record available to command-line demos, Tkinter, Flask, SQLite and TCP exercises.
- **Technology choices (source-derived, not proven historical intent):** Python keeps the course examples cohesive; SQLite is built in and file-based; Flask provides routes/templates; Tkinter supplies a standard-library desktop UI.
- **Useful properties:** small codebase, shared CRUD functions, explicit learning markers, runnable module demos.
- **Limitations:** no user authentication or CSRF protection, no schema migration framework, all web list rows are loaded at once, no formal tests, and some external/network features depend on services.
- **Contribution claims:** describe only work you personally performed and can support with a diff, history, or live explanation. The repository alone cannot establish individual authorship.

## 2. Architecture and code walkthrough questions

Each entry gives a direct response, a little more reasoning, code to point at, and a likely follow-up.

### Q: What runs first when the user starts the project?

**Direct answer:** `main.py` runs its `demo()` guard and enters `main()`. The menu imports only the selected module and calls its `demo()`.

**Explanation:** `MENU` stores module paths; `run_choice()` calls `importlib.import_module()`. The Flask app itself starts only when its module demo is selected or run with `python -m m5_apps.web`.

**Where:** `main.py`: `MENU`, `run_choice()`, `main()`.

**Follow-up:** Why lazy import? It keeps unrelated optional dependencies and blocking demos from loading just to display the menu.

### Q: How do the UI layers share data?

**Direct answer:** They call functions in `m3_data.database`, which uses the shared SQLite file.

**Explanation:** `database.py` returns ordinary dictionaries. `m5_apps.web` and `m5_apps.gui` add presentation/model behavior; `m4_network.server` queries the same CRUD layer. They do not each maintain a separate student store.

**Where:** `settings.DB_NAME`, `m3_data.database`, `m5_apps.web`, `m5_apps.gui`, `m4_network.server`.

**Follow-up:** What changes if the data backend changes? Keep the CRUD contract stable or update every caller and its tests together.

### Q: What happens during a Flask request?

**Direct answer:** `prepare_request()` configures logging and ensures the table and seed data exist, then Flask dispatches the requested route.

**Explanation:** Page and API handlers validate/convert inputs, call the database module, and render Jinja or return JSON. Form success uses flash plus redirect.

**Where:** `m5_apps/web.py`: `prepare_request()`, `_prepare_database()`, route handlers.

**Follow-up:** Why is database initialization on every request? It makes preview startup self-contained, but could be moved to explicit startup/migration work for larger applications.

### Q: What are the actual database constraints?

**Direct answer:** `roll` is the primary key; `name` and `marks` are `NOT NULL`.

**Explanation:** The table has no database-level marks range check or migration system. Application functions validate marks, but a different direct writer could bypass that validation.

**Where:** `m3_data/database.py`: `create_table()`, `_check_marks()`.

**Follow-up:** Does changing the `CREATE TABLE` statement alter an existing database? No; `IF NOT EXISTS` leaves the existing table as-is. A migration is required.

### Q: Is the web app authenticated?

**Direct answer:** No. Routes are publicly callable by anyone who can reach the process.

**Explanation:** `admin_only` checks a module-global demo role whose default is `"admin"`; it does not authenticate a browser or API caller. Forms also have no CSRF token.

**Where:** `m5_apps/web.py`; `m2_functional/decorators.py`: `CURRENT_ROLE`, `admin_only()`.

**Follow-up:** Can you deploy it publicly as-is? No. Add identity, authorization, CSRF protection, a strong secret and production server configuration first.

### Q: Why does the project use both SQLite and a socket protocol?

**Direct answer:** SQLite persists the shared records; the socket server is a separate networking exercise that demonstrates a simple text protocol.

**Explanation:** The server accepts newline-terminated messages and responds with a line such as `OK|10`. It is not a replacement for the Flask API and is unauthenticated.

**Where:** `m4_network/server.py`: `handle_command()`, `handle_client()`.

**Follow-up:** Why does it buffer pending text? TCP delivers a byte stream, not message boundaries; one `recv()` is not guaranteed to match one command.

## 3. Language and framework questions

### Python and object model

**Q: What is the difference between a class and an object here?** `Student` is the class; `Student(101, "Example", 78)` creates one object with its own roll/name/marks. `PASS_MARK` is a class attribute shared by the class.

**Q: What does double-underscore name mangling do?** `self.__marks` is renamed approximately to `_Student__marks`; it reduces accidental name collisions, but it is not a security boundary.

**Q: What do `@classmethod` and `@staticmethod` mean in this model?** `from_csv_row(cls, row)` receives the class and constructs it; `valid_roll(roll)` does not receive an implicit instance or class.

**Q: Is `__del__` deterministic?** No. Python does not guarantee exactly when an object is finalized. It is only a destructor demonstration in `person.py`.

### Functional and advanced Python

**Q: What is a higher-order function?** `apply_to_all(items, func)` accepts a function as a parameter. `map`, `filter`, and `reduce` demonstrate mapping, selection and folding.

**Q: What is the iterator protocol?** An iterator returns itself from `__iter__()` and produces values in `__next__()`, raising `StopIteration` when exhausted. `Classroom` implements it.

**Q: Why use a generator for database rows?** `student_rows()` yields one row at a time while its `DBConnection` context is active, rather than building a list first.

**Q: What does `nonlocal` do?** In `make_counter()`, it lets the nested `counter()` update the enclosing function's `count` variable.

**Q: What does a decorator do?** It replaces a function with a wrapper that can run behavior before/after the wrapped call. `functools.wraps` preserves useful metadata.

**Q: Why is `DBConnection` a context manager?** `__exit__()` commits on success, rolls back on an exception, closes the connection and returns `False` so exceptions are not suppressed.

**Q: What is a metaclass in this project?** `RegistryMeta`, deriving from `ABCMeta`, registers each class after its definition. `Person` uses it while retaining abstract-method enforcement.

### Flask, Jinja and the browser

**Q: What does a Flask route do?** It maps an HTTP path/method to a Python function. `@app.get("/api/students")` returns JSON; `/` renders `index.html`.

**Q: Why redirect after a successful form POST?** It follows the POST/redirect/GET pattern, reducing accidental resubmission on refresh.

**Q: Where is filtering performed?** In `static/js/app.js` against rows already rendered by Jinja. It is not SQL filtering, pagination, or access control.

**Q: Does the application use React/Vue or a frontend build?** No framework or bundler is configured; the frontend is Jinja-rendered HTML with plain CSS and JavaScript.

## 4. Feature-specific viva questions

### Student model and grade

**Q: What is the pass condition?** `marks >= Student.PASS_MARK`, default 40, in `Student.grade()`.

**Q: What is validated?** `Student.set_marks()` checks inclusive bounds 0–100 and raises `InvalidMarksError`. Flask and GUI have their own boundary validators; this duplication means changes must be coordinated.

**Q: What happens at exactly 40?** It passes because the comparison is greater-than-or-equal.

**Q: What do `Student.__lt__` and `__add__` mean?** They compare marks for sorting and return the sum of two marks, respectively—not a new student.

### Database and file handling

**Q: How does the seed avoid duplicate rows?** It returns without inserting when the student table count is nonzero. The count-and-insert is not a concurrency-safe migration.

**Q: Why parameterize SQL?** Values are passed separately from query text, avoiding unsafe string construction and treating input as data.

**Q: Why is untrusted pickle unsafe?** Unpickling can execute code encoded in malicious data. `restore_pickle()` is suitable only for trusted project-created backups.

**Q: Is `results.json` the live database?** No. SQLite is the shared record store; JSON is a file-handling demonstration output.

### Flask portal and API

**Q: Which API endpoints exist?** `GET /api/students`, `GET /api/students/<int:roll>`, and `POST /api/students`. No API update/delete route is present.

**Q: Where are marks changed/deleted?** Through `POST /student/<int:roll>` using form field `action=edit` or `action=delete`.

**Q: What is returned on missing API record?** `GET /api/students/<roll>` returns a JSON error with status 404.

**Q: Is the search field complete for a large dataset?** No. All rows render first and JavaScript hides non-matches in the browser.

### TCP, threading and external integrations

**Q: How does the socket server know where a message ends?** It uses newline delimiters and buffers partial chunks until a newline appears.

**Q: Why use a lock in the counter?** The increment is a read-modify-write operation. A lock keeps that critical section exclusive.

**Q: What does the report process do?** It reads DB rows, computes count/average/highest/pass percentage, and writes `data/report.txt`.

**Q: Does the email demo send mail by default?** No. `EMAIL_TEST_MODE=True` prints the `EmailMessage`; SMTP requires deliberate configuration and a password environment variable.

**Q: What is the scraper's failure behavior?** It catches `requests` request exceptions, but does not validate HTTP status before parsing. A successful HTTP response is not guaranteed to contain expected markup.

## 5. Code-level questions

| Question | Answer and symbol to point to | Likely follow-up |
|---|---|---|
| Why does `normalise_roll()` reject `True`? | `bool` subclasses `int`; it explicitly rejects bool before the integer check. | What other forms are accepted? Positive int, integral float and digit-only string. |
| What if `normalise_roll("101.0")` is called? | It raises `ValueError`; string input must be digit-only after trimming. | Should it accept decimals? Define the input contract and add tests before changing it. |
| What does `Student.from_csv_row()` convert? | Roll to `int`, marks through `int(float(...))`, then constructs the class. | Does this preserve fractional marks? No; it truncates after float conversion. |
| Why does `student_rows()` keep the DB context around its `yield`? | Iteration consumes rows while the `with DBConnection()` context is open; exhaustion/close exits the context. | What if the generator is abandoned early? Cleanup timing depends on generator close/finalization; explicitly close it when needed. |
| How does `search_students()` avoid SQL injection? | Search text is passed as bound parameters; `%` and `_` still act as SQL LIKE wildcards. | How can the search be literal? Escape wildcard characters and specify an escape character. |
| What is the empty report result? | `_average_mark` and `_pass_percentage` return 0 for count 0; `_highest_text(None)` returns `"None"`. | Add a test with an empty database. |
| What does `TeachingAssistant.__mro__` show? | The method-resolution sequence for multiple inheritance. | Why should you avoid guessing it? Python C3 MRO determines the actual method lookup order. |
| What errors does `api_add_student()` catch? | Integrity error and invalid marks/value/type conversion; returns a 400 JSON response. | What about a DB operational error? It is not handled there and may become a server error. |
| How does `app.run()` choose its endpoint? | It always binds to `127.0.0.1:5001`; `PORT` does not change the endpoint. Open the dashboard at `http://localhost:5001`. | Why not bind all interfaces? The unauthenticated teaching dashboard is intended for local use only. |
| What is the `COUNT` command complexity? | It fetches all row dictionaries and takes their length, so O(n) as written. | Could SQL `COUNT(*)` avoid transferring rows? Yes, an appropriate count query is more efficient. |

## 6. Database and API viva

### Schema and CRUD

- **Primary key:** integer `roll`.
- **Required columns:** `name TEXT NOT NULL`, `marks REAL NOT NULL`.
- **Foreign keys/indexes:** no foreign key; no explicit index besides SQLite's primary-key index.
- **Validation:** 0–100 marks checked in Python; no database `CHECK`.
- **CRUD SQL:** `INSERT`, `SELECT`, `UPDATE`, `DELETE`; all variable values use `?`.
- **Transactions:** each context-managed `DBConnection` commits or rolls back one unit of work. There is no transaction grouping across several function calls.
- **Migration:** no migration system. `CREATE TABLE IF NOT EXISTS` does not modify an existing table.

### HTTP interface

| Example | Expected behavior |
|---|---|
| `GET /api/students` | `200`, JSON list of student objects with roll, name, marks and grade |
| `GET /api/students/999` | `404`, JSON error if no such row |
| `POST /api/students` with valid JSON | `201`, created object |
| `POST /api/students` with duplicate roll or invalid marks | `400`, JSON error |
| `GET /student/999` | HTML 404 |
| `POST /student/101`, `action=edit`, valid marks | Redirect after update |
| `POST /student/101`, `action=delete` | Redirect after deletion (default demo role allows it) |

Request examples are in [README.md](README.md#example-requests). API routes currently have no authentication or rate limits. A `405 Method Not Allowed` is expected for methods not registered on a route; update/delete are not JSON API operations.

## 7. Algorithms and dry runs

### Pass/fail

For a mark `m`, return Pass if `m >= 40`, otherwise Fail. At 39: Fail. At 40: Pass. At 92: Pass. Time O(1), space O(1).

### Class total and grace marks

`class_total()` reduces marks from an initial total of zero. The ten sample values sum to 569. `add_grace()` adds 5 to each student with `min(100, marks + 5)`; the sample sum becomes 619 because none of the sample marks is above 95. It mutates student instances, so the demo clones its records first.

### Recursive structure walk

`total_marks(node)` has two recursive cases: for a list it totals the students, and for a dictionary it calls itself for every value; any other value contributes zero. The algorithm traverses the input once, O(n) in the visited structure, but very deep nesting can exceed Python recursion depth.

### Dashboard summary

Build the marks list, count `"Pass"` grades, compute arithmetic mean and maximum. For an empty list it returns count 0, pass rate 0, average 0 and highest `None`. The implementation performs a bounded number of full passes, so O(n) time and O(n) temporary storage.

### Counter with and without a lock

Two threads each increment a shared counter 100,000 times. Without a lock, each can read the same old value and overwrite another increment; actual results vary by scheduling. With `with lock:` around read, yield and write, expected result is 200,000. Do not claim the unlocked count is always wrong on every run.

## 8. Testing and debugging viva

### Core questions

**Unit vs integration vs end-to-end?** A unit test isolates a function/class; integration checks collaborating modules such as Flask plus SQLite; end-to-end checks the user-visible path in a browser/desktop. The repository has no formal suite today.

**What is coverage?** A measure of which code ran during tests; it does not prove assertions are correct. No coverage tool/configuration is present.

**How do you debug a failure?** Reproduce it with specific input, read the final exception and traceback frames, inspect values at the handler and persistence boundary, minimize the case, add a regression check, then rerun neighboring flows.

**How do you debug API behavior?** Start Flask, use a browser or HTTP client, inspect method/path/status/body, then trace to route → validation → database function. Use logs for unexpected errors.

**What is a regression test for changing the pass threshold?** Test exact boundary marks, summary pass rate, model grade, and TCP/report output that use the shared rule.

### Verified audit checks

- All 27 Python files passed in-memory syntax compilation.
- `python -m m2_functional.functional_tools` printed 3 failures, total 569 and grace total 619.
- A Flask test client using a temporary SQLite DB verified dashboard response, initial seed count, missing-record response, create, duplicate rejection, invalid marks rejection, update, delete and missing-after-delete.
- The TCP handler was checked with `COUNT`, `RESULT`, `QUIT` and an unknown command.
- No GUI/browser, live TCP socket, SMTP, MySQL, scraper, or thread/process run was performed.
- These were ad hoc audit checks; no test file was added and no formal test suite exists.

### Example failure diagnosis

| Symptom | First checks |
|---|---|
| API shows an empty list | Confirm working directory, `settings.DB_NAME`, CSV path and database initialization |
| Duplicate add returns 400 | Check roll primary key collision; read handler response before retrying |
| Marks accepted in one path but not another | Compare `Student.set_marks`, `database._check_marks`, GUI validator and Flask `_validate_values` |
| Client cannot connect to socket | Confirm server process, host and `SOCKET_PORT`; test `COUNT` locally |
| External API helper fails | Check Flask is running and inspect status/content type; JSON parsing errors are not covered by the request-exception catch |
| Flask session warning/forgery risk | Set a strong `SRM_SECRET_KEY`; the fallback string is for local teaching only |

## 9. Security and design-decision questions

**Q: What protects student records?** SQLite persistence and input checks exist, but the web app has no authentication, per-user authorization or CSRF tokens. Do not claim records are protected from unauthorized users.

**Q: Is the `admin_only` decorator real access control?** No. It reads a global string in a single Python process. There is no browser identity, session role, or API token check.

**Q: What is the most important pre-deployment change?** Establish a threat model and implement real authentication/authorization and CSRF defenses, then configure strong secrets and a production server. Do not expose a debug server.

**Q: How are SQL injection risks reduced?** CRUD values are bound as SQL parameters. Search wildcard semantics remain, but that is not SQL string injection.

**Q: What can go wrong with the backup?** Pickle is executable during deserialization; backup writes are not atomic; no scheduled production-grade backup or restore verification exists.

**Q: How would the project scale?** Add server-side pagination and indexes, connection/error strategy, migration tooling, and a production DB/service architecture. These are proposals, not current capabilities.

**Q: What design intent is certain?** The course context explains that student marks are a teaching domain; other original motivations should not be asserted unless the developer confirms them.

**Q: What is the weakest implementation area?** A defensible answer is security and test automation: the web routes are unauthenticated, forms lack CSRF protection, and there is no formal automated suite.

## 10. Practical modification challenges

Each task below is a proposed examination exercise. The instructions are not claims that the modification has already been applied.

### Challenge A — Change the pass mark to 50

1. **Request/testing:** “Make 50 the pass threshold.” Tests class-attribute behavior and regression tracing.
2. **Files:** `m1_oop/student.py`, then check dependent views/reports/socket behavior.
3. **Plan:** edit `Student.PASS_MARK`, inspect consumers, verify 49 fails and 50 passes.
4. **Exact edit:**

```python
PASS_MARK = 50  # CHANGE ME: pass mark
```

5. **Dependencies:** `Student.grade()` drives Flask and GUI status; socket `_grade_for()` reads the class rule; report `_pass_mark()` reads it; the functional demo's expected failure count changes.
6. **Tests:** run `python -m m2_functional.functional_tools`; add/execute boundary checks for 49 and 50; check dashboard and TCP result when available.
7. **Expected:** five of the sample records fail at threshold 50, per the sample data.
8. **Common mistake:** editing only a displayed label or duplicating a different threshold into a UI.
9. **Follow-up:** What happens if marks equal the threshold? They pass (`>=`).

### Challenge B — Add strict marks validation to the JSON API

1. **Request/testing:** Reject JSON booleans and strings as marks rather than silently coercing them.
2. **Files:** `m5_apps/web.py` (`_validate_values()` and API handler); preferably add tests in a new test module.
3. **Plan:** define accepted JSON types; preserve HTML form conversion separately; reject booleans before `float()`; test numbers, boolean, string, missing and out-of-range values.
4. **Illustrative targeted guard** (adapt to distinguish JSON from HTML input; not existing code):

```python
if isinstance(marks_value, bool):
    raise ValueError("Marks must be a number.")
marks = float(marks_value)
```

5. **Dependencies:** keep friendly error mapping and API status 400; do not break normal HTML form values, which arrive as strings.
6. **Tests:** `POST /api/students` with `true`, `"73"`, `73`, missing, `-1`, `101`, and valid decimal values.
7. **Expected:** only the types allowed by the chosen contract succeed.
8. **Common mistake:** apply a JSON-only rule to form input, which is text by definition.
9. **Follow-up:** Why reject bool? In Python, `bool` is a subclass of `int`, but it is not a meaningful mark.

### Challenge C — Add a regression test for roll normalization

1. **Request/testing:** Cover positive integers, integer strings, integral floats, bool, zero, negatives and malformed input.
2. **Files:** add a `unittest` or chosen test file importing `m2_functional.scope_demo.normalise_roll`.
3. **Plan:** write assertions for the accepted contract and expected `ValueError` cases; run the focused test and suite.
4. **Proposed example test** (new file, not currently present):

```python
import unittest

from m2_functional.scope_demo import normalise_roll


class NormaliseRollTests(unittest.TestCase):
    def test_accepts_positive_integer_forms(self):
        self.assertEqual(normalise_roll("101 "), 101)
        self.assertEqual(normalise_roll(101.0), 101)

    def test_rejects_bool_and_non_positive_values(self):
        for value in (True, 0, -1, "101.0", "bad"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalise_roll(value)
```

5. **Expected:** run with `python -m unittest discover -s tests`.
6. **Common mistake:** test only a happy path or assert on an exact exception message when message wording is not part of the contract.
7. **Follow-up:** Why not use `assert` for user input? Assertions can be disabled with optimized Python and are intended for programmer invariants.

### Challenge D — Add server-side filtering to the REST list (proposed)

1. **Request/testing:** support `GET /api/students?query=...` without requiring the browser to download every row.
2. **Files:** `m5_apps/web.py` (`api_students()`), `m3_data/database.py` (`search_students()`), tests and API documentation.
3. **Plan:** read/trim the query, choose `get_all_students()` for empty query or `search_students(query)` otherwise, preserve ordered JSON response and document wildcard behavior.
4. **Proposed handler shape** (not existing):

```python
@app.get("/api/students")
def api_students():
    query = request.args.get("query", "").strip()
    rows = database.search_students(query) if query else database.get_all_students()
    return jsonify([_student(row) for row in rows])
```

5. **Tests:** no query returns all; query matches name and roll; empty query; no match; wildcard behavior.
6. **Expected:** filtered results are returned from SQLite before JSON conversion.
7. **Common mistake:** assume current JavaScript filtering already filters the server-side API.
8. **Follow-up:** What should be added for a large dataset? Pagination and explicit limits.

### Challenge E — Add a database field safely

1. **Request/testing:** add a real field such as `email`; this is a cross-layer schema change, not one template edit.
2. **Files:** `m1_oop/student.py`, `m3_data/database.py`, `m3_data/files.py`, `m5_apps/gui.py`, `m5_apps/web.py`, templates, seed CSV, API expectations and tests.
3. **Plan:** specify nullable/unique rules; write a migration for existing DB; change row conversion and SQL; update CSV and forms; update serializers; test old and new data.
4. **Expected:** old records remain readable, new values validate and persist, and all interfaces expose a consistent field.
5. **Common mistake:** changing only `CREATE TABLE IF NOT EXISTS` and assuming the existing DB schema changes automatically.
6. **Follow-up:** How do you protect existing user data? Back up the database and run a versioned migration rather than deleting it.

## 11. Testing scenario bank

These are recommended scenarios unless the status column says otherwise.

| Scenario | Setup | Action | Expected result / internal behavior | Verification |
|---|---|---|---|---|
| Seed database | Empty isolated DB and valid CSV | Create table and call seed twice | First call inserts sample rows; second inserts none | Execute CRUD checks |
| Valid create | Unique positive roll | Submit valid marks/name | Insert commits; row appears on list | Flask test client or API |
| Duplicate create | Existing roll | Submit same roll | Primary-key conflict becomes friendly 400 | **API case verified** |
| Invalid marks | Existing app/test client | Submit -1, 101, missing, nonnumeric | No invalid write; error returned | >100 API case verified; other boundaries suggested |
| Pass boundary | Student marks 39, 40, 41 | Call `grade()` | Fail, Pass, Pass at threshold 40 | Add unit test |
| Missing row | No roll 999 | API GET or page GET | JSON 404 or page 404 | **API 404 verified** |
| Update marks | Existing student | POST `action=edit` | Update commits and redirects | **Verified with isolated DB** |
| Delete row | Existing student | POST `action=delete` | Delete commits and redirects | **Verified with isolated DB** |
| Search/filter | Rendered dashboard | Type text / select status | JS hides rows and changes count | Browser scenario, not run |
| Empty database report | Empty DB | Run report | Zero average/pass rate, no highest | Source-derived; not run |
| Missing Flask service | Server stopped | Call `fetch_students_from_api()` | Prints start-app guidance and returns empty list on request error | Not run |
| Invalid API JSON response | API client receives non-JSON | Call API helper | Current JSON decode failure may propagate | Suggested failure test; robustness gap |
| Socket unknown command | Server handler | Send arbitrary command | <code>ERROR&#124;Unknown command</code> | **Handler case verified** |
| Socket split packet | Live local connection | Send command across chunks | Buffering should wait for newline | Not tested with live socket |
| Unauthorized mutation | Reach deployed app as anonymous user | POST add/edit/delete | Current implementation has no identity gate | Static security finding; do not test against public system |
| Concurrent seed | Two initial requests to empty DB | Both count then insert | Possible primary-key race | Source-derived risk; not stress-tested |
| Tkinter workflow | Desktop with Tk available | Add, select, edit marks, delete, search | Table/status update and errors display | Not run |
| SMTP/MySQL unavailable | Test environment only | Run optional demo with service absent | Email stays print-only; MySQL reports skip on import/connect failure | Not executed |

## 12. Examiner challenge questions

**Why did you implement this way?** The source uses small concept-oriented modules and a shared CRUD layer. Avoid claiming a historical rationale beyond what the course specification states.

**What if the database is empty?** Startup/request setup creates the table and tries to seed from the configured CSV; that file is expected to exist, and a missing/unreadable file is not silently ignored. Report calculations themselves handle zero rows.

**What if two people add the same roll?** SQLite primary key allows one insert; the other gets `IntegrityError`, which Flask/GUI handle in their add flows. Concurrent seed remains a race.

**What if input is malformed?** Form/API validation handles common missing, range and conversion errors; edge types such as JSON bools are not explicitly rejected.

**Can delete be bypassed?** The confirmation dialog can be bypassed because it is client-side UX. There is also no authenticated authorization; the backend decorator checks a process-global default role.

**What is the time complexity of listing/search?** Both list and current search are O(n)-style scans for ordinary use; search has no supporting name index and dashboard loads every row.

**How do you prove a modification is correct?** Define behavior and boundaries, assert the result in focused tests, then exercise the integration and regression paths. Do not rely only on a screenshot.

**What would you improve first?** Add real access control/CSRF if it is to be network-accessible; add automated tests and migrations for maintainability.

**What claims were actually verified?** Syntax of all 27 Python files, functional demo totals, selected Flask CRUD/API flows, and TCP command-handler replies in an isolated temporary database. Browser, GUI, real socket, and external services were not verified.

## 13. Rapid revision sheet

### Memorize this structure

- **Entry:** `main.py`; 19 lazy demo entries.
- **Domain:** `m1_oop/student.py`: `Student`, marks 0–100, pass mark 40.
- **Data:** `m3_data/database.py`; SQLite table `students(roll, name, marks)`.
- **Connection lifecycle:** `m2_functional/context_meta.py`: `DBConnection`.
- **Web:** `m5_apps/web.py`; `/`, `/student/<roll>`, `/add`, three JSON endpoints, route manifest.
- **GUI:** `m5_apps/gui.py`; Tkinter `App`.
- **Network:** `m4_network/server.py` and `client.py`; line-delimited TCP port 5050.
- **Seed values:** 10 records, total 569, average 56.9, highest 92, 3 fail at threshold 40, grace total 619.
- **Dependency constraints:** Flask 3.x, requests 2.x, Beautiful Soup 4.x; SQLite and Tkinter from Python/platform.
- **Security warning:** no authentication or CSRF protection; fixed Flask secret fallback; keep local only.

### Demonstration commands

```text
python main.py
python -m m3_data.database
python -m m2_functional.functional_tools
python -m m5_apps.web
python -m m5_apps.gui
python -m m4_network.server
python -m m4_network.client
```

### Five strengths

1. Coherent domain reused across modules.
2. Shared parameterized SQLite CRUD rather than duplicate SQL in each UI.
3. Useful runnable demonstrations with explicit `demo()` entry points.
4. Simple separation between data, model, UI and network examples.
5. Clear expected-value checks for sample functional data.

### Five honest limitations

1. No authentication, authorization for real users or CSRF defense.
2. No formal automated test suite or coverage report.
3. No migration framework or DB-level mark range constraint.
4. REST API has no pagination and lacks update/delete endpoints.
5. External-service, GUI/browser, and concurrency behavior was not fully exercised.

### Commonly confused concepts

- **Authentication vs authorization:** who the user is vs what they may do; neither is implemented for web users.
- **Primary key vs validation:** roll uniqueness is enforced by SQLite; mark range is application validation only.
- **HTTP API vs HTML form:** JSON endpoints only list/read/create; edit/delete use HTML form POST.
- **Thread vs process:** thread shares process memory; process has a separate address space.
- **Iterator vs generator:** `Classroom` implements iterator methods; `student_rows()` is a generator function using `yield`.
- **Name mangling vs security:** name mangling discourages accidental access; it does not protect secrets.
- **Assertion vs input validation:** assertions express programmer assumptions; use exceptions for user input.
- **Pickling vs safe interchange:** pickle is Python-specific and unsafe for untrusted content; JSON/CSV are text formats.

### Final pre-viva checklist

- [ ] Start from the repository root and verify Python/dependencies.
- [ ] Know whether the DB contains old demo data; back it up before reset.
- [ ] Be able to trace one request from UI to route to `database.py` and back.
- [ ] Explain exact boundaries: 0–100 marks, pass at `>= 40`, roll positive whole number.
- [ ] Know the difference between Flask page POST and REST API methods.
- [ ] Demonstrate one normal path and one invalid-input path.
- [ ] Do not claim the application is secure or production-ready.
- [ ] Distinguish verified results from source-derived behavior and proposed improvements.
- [ ] Never show real credentials or use live external email during a demonstration.
