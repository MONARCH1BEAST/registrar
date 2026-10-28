"""SQLite data access for the assignment registrar."""
import sqlite3, settings; from datetime import datetime
from m2_functional.context_meta import DBConnection
# CONCEPT: SQLite connectivity and CRUD
def create_table():
    with DBConnection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS batches (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, year TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS students (roll TEXT PRIMARY KEY, name TEXT NOT NULL, batch_id INTEGER NOT NULL REFERENCES batches(id))")
        conn.execute("CREATE TABLE IF NOT EXISTS assignments (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, max_marks REAL NOT NULL, due_date TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY AUTOINCREMENT, assignment_id INTEGER NOT NULL, roll TEXT NOT NULL, marks REAL NOT NULL, submitted_on TEXT NOT NULL, FOREIGN KEY(assignment_id) REFERENCES assignments(id) ON DELETE CASCADE, FOREIGN KEY(roll) REFERENCES students(roll), UNIQUE(assignment_id, roll))")
        _migrate_batches(conn)
        roll_type = next(row["type"] for row in conn.execute("PRAGMA table_info(students)") if row["name"] == "roll")
        if roll_type.upper() != "TEXT":
            _migrate_roll_columns(conn)
def _migrate_batches(conn):
    columns = [row["name"] for row in conn.execute("PRAGMA table_info(students)")]
    if "batch_id" in columns:
        return
    conn.execute("ALTER TABLE students ADD COLUMN batch_id INTEGER REFERENCES batches(id)")
    if conn.execute("SELECT 1 FROM students LIMIT 1").fetchone():
        batch_id = conn.execute("INSERT INTO batches (name, year) VALUES (?, ?)", ("Legacy batch", "Legacy")).lastrowid
        conn.execute("UPDATE students SET batch_id = ?", (batch_id,))
    conn.execute("CREATE TRIGGER IF NOT EXISTS students_batch_required_insert BEFORE INSERT ON students WHEN NEW.batch_id IS NULL BEGIN SELECT RAISE(ABORT, 'batch_id is required'); END")
    conn.execute("CREATE TRIGGER IF NOT EXISTS students_batch_required_update BEFORE UPDATE OF batch_id ON students WHEN NEW.batch_id IS NULL BEGIN SELECT RAISE(ABORT, 'batch_id is required'); END")
def _migrate_roll_columns(conn):
    conn.execute("PRAGMA defer_foreign_keys = ON")
    conn.execute("CREATE TABLE students_text (roll TEXT PRIMARY KEY, name TEXT NOT NULL, batch_id INTEGER NOT NULL REFERENCES batches(id))")
    conn.execute("INSERT INTO students_text SELECT CAST(roll AS TEXT), name, batch_id FROM students")
    conn.execute("CREATE TABLE submissions_text (id INTEGER PRIMARY KEY AUTOINCREMENT, assignment_id INTEGER NOT NULL, roll TEXT NOT NULL, marks REAL NOT NULL, submitted_on TEXT NOT NULL, FOREIGN KEY(assignment_id) REFERENCES assignments(id) ON DELETE CASCADE, FOREIGN KEY(roll) REFERENCES students_text(roll), UNIQUE(assignment_id, roll))")
    conn.execute("INSERT INTO submissions_text SELECT id, assignment_id, CAST(roll AS TEXT), marks, submitted_on FROM submissions")
    conn.execute("DROP TABLE submissions")
    conn.execute("DROP TABLE students")
    conn.execute("ALTER TABLE students_text RENAME TO students")
    conn.execute("ALTER TABLE submissions_text RENAME TO submissions")
def _check_date(value):
    if datetime.strptime(value, settings.DATE_FORMAT).strftime(settings.DATE_FORMAT) != value: raise ValueError("date must use " + settings.DATE_FORMAT)
def add_batch(name, year):
    with DBConnection() as conn:
        cursor = conn.execute("INSERT INTO batches (name, year) VALUES (?, ?)", (name, year))
    return get_batch(cursor.lastrowid)
def delete_batch(batch_id):
    with DBConnection() as conn:
        conn.execute("DELETE FROM submissions WHERE roll IN (SELECT roll FROM students WHERE batch_id = ?)", (batch_id,))
        conn.execute("DELETE FROM students WHERE batch_id = ?", (batch_id,))
        return conn.execute("DELETE FROM batches WHERE id = ?", (batch_id,)).rowcount > 0
def get_all_batches():
    query = "SELECT b.id, b.name, b.year, COUNT(s.roll) AS student_count FROM batches b LEFT JOIN students s ON s.batch_id = b.id GROUP BY b.id ORDER BY b.name, b.year"
    with DBConnection() as conn:
        rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]
def get_batch(batch_id):
    query = "SELECT b.id, b.name, b.year, COUNT(s.roll) AS student_count FROM batches b LEFT JOIN students s ON s.batch_id = b.id WHERE b.id = ? GROUP BY b.id"
    with DBConnection() as conn:
        row = conn.execute(query, (batch_id,)).fetchone()
    return dict(row) if row else None
def get_students_by_batch(batch_id):
    query = "SELECT st.roll, st.name, COUNT(s.id) AS submission_count FROM students st LEFT JOIN submissions s ON s.roll = st.roll WHERE st.batch_id = ? GROUP BY st.roll, st.name ORDER BY st.roll"
    with DBConnection() as conn:
        rows = conn.execute(query, (batch_id,)).fetchall()
    return [dict(row) for row in rows]
def add_student(roll, name, batch_id):
    with DBConnection() as conn:
        conn.execute("INSERT INTO students (roll, name, batch_id) VALUES (?, ?, ?)", (roll, name, batch_id))
    return {"roll": roll, "name": name, "batch_id": batch_id}
def get_student(roll):
    with DBConnection() as conn: row = conn.execute("SELECT st.roll, st.name, COALESCE((SELECT marks FROM submissions WHERE roll = st.roll ORDER BY id DESC LIMIT 1), 0) AS marks FROM students st WHERE st.roll = ?", (roll,)).fetchone()
    return dict(row) if row else None
def add_students_bulk(student_list, batch_id):
    rows = [(roll, name, batch_id) for roll, name in student_list]
    with DBConnection() as conn:
        conn.executemany("INSERT OR IGNORE INTO students (roll, name, batch_id) VALUES (?, ?, ?)", rows)
        return conn.total_changes
def delete_student_by_batch(roll, batch_id):
    with DBConnection() as conn:
        conn.execute("DELETE FROM submissions WHERE roll = ? AND roll IN (SELECT roll FROM students WHERE batch_id = ?)", (roll, batch_id))
        cursor = conn.execute("DELETE FROM students WHERE roll = ? AND batch_id = ?", (roll, batch_id))
    return cursor.rowcount > 0
def delete_students_bulk_by_batch(rolls, batch_id):
    if not rolls:
        return 0
    with DBConnection() as conn:
        valid = []
        for roll in rolls:
            row = conn.execute("SELECT roll FROM students WHERE roll = ? AND batch_id = ?", (roll, batch_id)).fetchone()
            if row: valid.append(row["roll"])
        conn.executemany("DELETE FROM submissions WHERE roll = ?", [(roll,) for roll in valid])
        conn.executemany("DELETE FROM students WHERE roll = ? AND batch_id = ?", [(roll, batch_id) for roll in valid])
    return len(valid)
def delete_all_students_by_batch(batch_id):
    with DBConnection() as conn:
        rolls = [row["roll"] for row in conn.execute("SELECT roll FROM students WHERE batch_id = ?", (batch_id,)).fetchall()]
        conn.executemany("DELETE FROM submissions WHERE roll = ?", [(roll,) for roll in rolls])
        cursor = conn.execute("DELETE FROM students WHERE batch_id = ?", (batch_id,))
    return cursor.rowcount
def delete_student(roll):
    try:
        with DBConnection() as conn: conn.execute("DELETE FROM submissions WHERE roll = ?", (roll,)); cursor = conn.execute("DELETE FROM students WHERE roll = ?", (roll,))
        return cursor.rowcount > 0
    except sqlite3.IntegrityError as error:
        raise ValueError("Student could not be deleted because related records remain.") from error
def delete_students_bulk(rolls):
    if not rolls: return 0
    placeholders = ", ".join("?" for _ in rolls)
    with DBConnection() as conn:
        conn.execute(f"DELETE FROM submissions WHERE roll IN ({placeholders})", rolls)
        cursor = conn.execute(f"DELETE FROM students WHERE roll IN ({placeholders})", rolls)
        return cursor.rowcount
def delete_all_students():
    with DBConnection() as conn:
        conn.execute("DELETE FROM submissions")
        cursor = conn.execute("DELETE FROM students")
        return cursor.rowcount
def get_all_students():
    with DBConnection() as conn: return [dict(row) for row in conn.execute("SELECT roll, name, batch_id FROM students ORDER BY roll").fetchall()]
def get_students_with_submission_counts():
    with DBConnection() as conn: return [dict(row) for row in conn.execute("SELECT st.roll, st.name, COUNT(s.id) AS submission_count FROM students st LEFT JOIN submissions s ON s.roll = st.roll GROUP BY st.roll, st.name ORDER BY st.roll").fetchall()]
def add_assignment(title, max_marks, due_date):
    _check_date(due_date)
    with DBConnection() as conn: cursor = conn.execute("INSERT INTO assignments (title, max_marks, due_date) VALUES (?, ?, ?)", (title, max_marks, due_date))
    return get_assignment(cursor.lastrowid)
def get_all_assignments():
    with DBConnection() as conn: return [dict(row) for row in conn.execute("SELECT a.id, a.title, a.max_marks, a.due_date, COUNT(s.id) AS submission_count FROM assignments a LEFT JOIN submissions s ON s.assignment_id = a.id GROUP BY a.id ORDER BY a.id").fetchall()]
def get_assignment(id):
    with DBConnection() as conn: row = conn.execute("SELECT id, title, max_marks, due_date FROM assignments WHERE id = ?", (id,)).fetchone(); return dict(row) if row else None
def delete_assignment(assignment_id):
    with DBConnection() as conn:
        return conn.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,)).rowcount > 0
def add_submission(assignment_id, roll, marks, submitted_on):
    _check_date(submitted_on)
    with DBConnection() as conn: cursor = conn.execute("INSERT INTO submissions (assignment_id, roll, marks, submitted_on) VALUES (?, ?, ?, ?)", (assignment_id, roll, marks, submitted_on)); return dict(conn.execute("SELECT s.id, s.assignment_id, s.roll, st.name, s.marks, s.submitted_on FROM submissions s JOIN students st ON st.roll = s.roll WHERE s.id = ?", (cursor.lastrowid,)).fetchone())
def get_submissions_for_assignment(assignment_id):
    with DBConnection() as conn: return [dict(row) for row in conn.execute("SELECT s.id, s.assignment_id, s.roll, st.name, s.marks, s.submitted_on FROM submissions s JOIN students st ON st.roll = s.roll WHERE s.assignment_id = ? ORDER BY s.id", (assignment_id,)).fetchall()]
def get_submission(id):
    with DBConnection() as conn: row = conn.execute("SELECT id, assignment_id, roll, marks, submitted_on FROM submissions WHERE id = ?", (id,)).fetchone(); return dict(row) if row else None
def update_submission_marks(id, marks):
    with DBConnection() as conn: return conn.execute("UPDATE submissions SET marks = ? WHERE id = ?", (marks, id)).rowcount > 0
def delete_submission(id):
    with DBConnection() as conn: return conn.execute("DELETE FROM submissions WHERE id = ?", (id,)).rowcount > 0

def demo():
    create_table(); print("Students:", get_all_students()); print("Assignments:", get_all_assignments())
if __name__ == "__main__": demo()
