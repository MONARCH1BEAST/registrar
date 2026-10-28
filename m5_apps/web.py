"""Flask pages and JSON API for the assignment registrar."""
import csv, io, os, sqlite3, settings; from datetime import date
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for
from m3_data import database; from m3_data.exceptions import InvalidMarksError; from m1_oop.student import Student
from m3_data.files import load_config; from m3_data.logger import setup_logging
# CONCEPT: Flask routing, templates, forms, and REST APIs
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SRM_SECRET_KEY", "registrar-demo")
@app.before_request
def prepare_request(): setup_logging(); database.create_table()
@app.context_processor
def shared_context():
    try: config = load_config()
    except (OSError, ValueError): config = {"school": "University", "year": ""}
    return {"school": config.get("school", "University"), "academic_year": config.get("year", "")}
def _assignment(id): return database.get_assignment(id) or abort(404)
def _batch(batch_id):
    return database.get_batch(batch_id) or abort(404)
@app.get("/")
def index():
    rows = database.get_all_assignments(); today = date.today().strftime(settings.DATE_FORMAT); summary = {"assignments": len(rows), "submissions": sum(r["submission_count"] for r in rows), "upcoming": sum(r["due_date"] >= today for r in rows)}; return render_template("index.html", assignments=rows, summary=summary)
@app.route("/add_assignment", methods=["GET", "POST"])
def add_assignment():
    if request.method == "POST":
        try:
            title, marks, due = request.form["title"].strip(), float(request.form["max_marks"]), request.form["due_date"]
            if not title or marks <= 0: raise ValueError("Enter a title and positive maximum marks.")
            database.add_assignment(title, marks, due); flash("Assignment added.", "success"); return redirect(url_for("index"))
        except (KeyError, TypeError, ValueError) as error: return render_template("add_assignment.html", form_error=str(error), values=request.form), 400
    return render_template("add_assignment.html", values={})
@app.get("/students")
def students():
    return redirect(url_for("batches"))
@app.get("/batches")
def batches():
    return render_template("batches.html", batches=database.get_all_batches())
@app.post("/add_batch")
def add_batch():
    try:
        name, year = request.form["name"].strip(), request.form["year"].strip()
        if not name or not year:
            raise ValueError("Enter a batch name and year.")
        database.add_batch(name, year)
        flash("Batch added.", "success")
    except (KeyError, TypeError, ValueError) as error:
        flash(str(error), "error")
    return redirect(url_for("batches"))
@app.post("/batch/delete/<int:batch_id>")
def delete_batch(batch_id):
    _batch(batch_id)
    database.delete_batch(batch_id)
    flash("Batch deleted successfully.", "success")
    return redirect(url_for("batches"))
@app.get("/batch/<int:batch_id>")
def batch_detail(batch_id):
    batch = _batch(batch_id)
    return render_template("batch_detail.html", batch=batch, students=database.get_students_by_batch(batch_id))
@app.post("/batch/<int:batch_id>/student/delete/<string:roll>")
def delete_student(batch_id, roll):
    _batch(batch_id)
    deleted = database.delete_student_by_batch(roll, batch_id)
    flash("Student deleted successfully." if deleted else "Student not found in this batch.", "success" if deleted else "error")
    return redirect(url_for("batch_detail", batch_id=batch_id))
@app.post("/batch/<int:batch_id>/delete_selected")
def delete_selected(batch_id):
    _batch(batch_id)
    rolls = request.form.getlist("selected_students")
    if not rolls:
        flash("Select at least one student to delete.", "error")
    else:
        deleted = database.delete_students_bulk_by_batch(rolls, batch_id)
        flash(f"{deleted} students deleted.", "success")
    return redirect(url_for("batch_detail", batch_id=batch_id))
@app.post("/batch/<int:batch_id>/clear_all_students")
def clear_all_students(batch_id):
    _batch(batch_id)
    database.delete_all_students_by_batch(batch_id)
    flash("All students cleared", "warning")
    return redirect(url_for("batch_detail", batch_id=batch_id))
def parse_student_csv(file):
    reader = csv.reader(io.StringIO(file.stream.read().decode("utf-8-sig"))); first = next(reader, [])
    headers = [value.strip().lower() for value in first]; ri = next((i for i, value in enumerate(headers) if "roll" in value), None); ni = next((i for i, value in enumerate(headers) if "name" in value), None); rows = list(reader)
    if ri is None or ni is None: ri, ni, rows = 0, 1, [first] + rows
    students = [(row[ri].strip(), row[ni].strip()) for row in rows if len(row) > max(ri, ni) and Student.valid_roll(row[ri].strip()) and row[ni].strip()]
    return students, len(rows)
@app.post("/batch/<int:batch_id>/import_students")
def import_students(batch_id):
    _batch(batch_id)
    upload = request.files.get("csv_file")
    if not upload or not upload.filename:
        flash("Choose a CSV file to import.", "error")
        return redirect(url_for("batch_detail", batch_id=batch_id))
    try:
        students, total = parse_student_csv(upload)
        imported = database.add_students_bulk(students, batch_id)
        flash(f"{imported} students imported, {total - imported} skipped.", "success")
    except (UnicodeDecodeError, csv.Error, TypeError, ValueError) as error:
        flash("CSV import failed: {}".format(error), "error")
    return redirect(url_for("batch_detail", batch_id=batch_id))
@app.route("/batch/<int:batch_id>/add_student", methods=["GET", "POST"])
def add_student(batch_id):
    batch = _batch(batch_id)
    if request.method == "POST":
        try:
            _save_student(batch_id)
        except sqlite3.IntegrityError:
            flash("Roll number already exists.", "error")
            return render_template("add_student.html", batch=batch, values=request.form), 400
        except (KeyError, TypeError, ValueError) as error:
            flash(str(error), "error")
            return render_template("add_student.html", batch=batch, values=request.form), 400
        flash("Student added successfully.", "success")
        return redirect(url_for("batch_detail", batch_id=batch_id))
    return render_template("add_student.html", batch=batch, values={})
def _save_student(batch_id):
    roll, name = request.form["roll"].strip(), request.form["name"].strip()
    if not Student.valid_roll(roll) or not name:
        raise ValueError("Enter a valid roll ID and student name.")
    database.add_student(roll, name, batch_id)
@app.get("/assignment/<int:id>")
def assignment_detail(id): return render_template("assignment.html", assignment=_assignment(id), submissions=database.get_submissions_for_assignment(id))
@app.post("/assignment/delete/<int:assignment_id>")
def delete_assignment(assignment_id):
    _assignment(assignment_id)
    database.delete_assignment(assignment_id)
    flash("Assignment deleted successfully.", "success")
    return redirect(url_for("index"))
@app.route("/assignment/<int:id>/submit", methods=["GET", "POST"])
def add_submission(id):
    assignment = _assignment(id)
    batches = database.get_all_batches()
    students = database.get_all_students()
    if request.method == "POST":
        selected_roll = request.form.get("roll", "")
        selected_student = next((student for student in students if str(student["roll"]) == selected_roll), None)
        selected_batch_id = selected_student["batch_id"] if selected_student else ""
        try:
            roll, marks, submitted = request.form["roll"].strip(), float(request.form["marks"]), request.form["submitted_on"]
            if not 0 <= marks <= assignment["max_marks"]: raise InvalidMarksError("Marks exceed the assignment maximum.")
            database.add_submission(id, roll, marks, submitted); flash("Submission added.", "success"); return redirect(url_for("assignment_detail", id=id))
        except sqlite3.IntegrityError: return render_template("add_submission.html", assignment=assignment, batches=batches, students=students, selected_batch_id=selected_batch_id, form_error="Student already submitted or does not exist.", values=request.form), 400
        except (KeyError, TypeError, ValueError, InvalidMarksError) as error: return render_template("add_submission.html", assignment=assignment, batches=batches, students=students, selected_batch_id=selected_batch_id, form_error=str(error), values=request.form), 400
    return render_template("add_submission.html", assignment=assignment, batches=batches, students=students, selected_batch_id="", values={})
@app.post("/submission/delete/<int:id>")
def remove_submission(id):
    row = database.get_submission(id)
    if row is None or not database.delete_submission(id): abort(404)
    flash("Submission deleted.", "success"); return redirect(url_for("assignment_detail", id=row["assignment_id"]))
@app.get("/api/assignments")
def api_assignments(): return jsonify(database.get_all_assignments())
@app.get("/api/students")
def api_students(): return jsonify(database.get_all_students())
@app.get("/api/students/<string:roll>")
def api_student(roll): return jsonify(database.get_student(roll) or abort(404))
@app.get("/api/assignments/<int:id>/submissions")
def api_submissions(id): _assignment(id); return jsonify(database.get_submissions_for_assignment(id))
def demo(): app.run(host=settings.HOST, port=settings.FLASK_PORT, debug=True)
if __name__ == "__main__": demo()
