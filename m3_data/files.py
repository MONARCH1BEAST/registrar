"""CSV, JSON, pickle, and activity-file helpers for assignment data."""
import csv, json, os, pickle
from datetime import datetime; import settings

def _ensure_parent(path):
    if os.path.dirname(path): os.makedirs(os.path.dirname(path), exist_ok=True)

def write_activity(text):
    _ensure_parent(settings.ACTIVITY_FILE); f = open(settings.ACTIVITY_FILE, "a", encoding="utf-8")
    with f: f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | " + text + "\n")

def read_activity():
    try:
        with open(settings.ACTIVITY_FILE, encoding="utf-8") as f: return f.readlines()
    except FileNotFoundError: return []

def export_csv(data):
    _ensure_parent(settings.CSV_EXPORT)
    assignments = {a["id"]: a for a in data["assignments"]}
    fields = ["assignment_id", "assignment_title", "roll", "student_name", "marks", "submitted_on"]
    with open(settings.CSV_EXPORT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
        for s in data["submissions"]:
            writer.writerow(dict(assignment_id=s["assignment_id"], assignment_title=assignments[s["assignment_id"]]["title"], roll=s["roll"], student_name=s["name"], marks=s["marks"], submitted_on=s["submitted_on"]))

def import_csv():
    with open(settings.CSV_IMPORT, newline="", encoding="utf-8") as f: return [{**r, "max_marks": float(r["max_marks"]), "roll": r["roll"].strip(), "marks": float(r["marks"])} for r in csv.DictReader(f)]

def save_json(data):
    _ensure_parent(settings.JSON_FILE); nested = [dict(a, submissions=[{k: s[k] for k in ("roll", "name", "marks", "submitted_on")} for s in data["submissions"] if s["assignment_id"] == a["id"]]) for a in data["assignments"]]
    with open(settings.JSON_FILE, "w", encoding="utf-8") as f: json.dump(nested, f, indent=2)

def load_json():
    with open(settings.JSON_FILE, encoding="utf-8") as f: return json.load(f)

def load_config():
    with open(settings.CONFIG_FILE, encoding="utf-8") as f: return json.load(f)

def backup_pickle(data):
    if not isinstance(data, dict) or not {"assignments", "submissions"} <= data.keys(): raise ValueError("backup data must contain assignments and submissions")
    _ensure_parent(settings.BACKUP_FILE)
    with open(settings.BACKUP_FILE, "wb") as f: pickle.dump(data, f)

def restore_pickle():
    with open(settings.BACKUP_FILE, "rb") as f: return pickle.load(f)

def get_export_data():
    from m3_data import database
    assignments = database.get_all_assignments(); submissions = [s for a in assignments for s in database.get_submissions_for_assignment(a["id"])]
    return {"assignments": assignments, "submissions": submissions}

def demo():
    from m3_data import database
    database.create_table(); data = get_export_data()
    export_csv(data); save_json(data); backup_pickle(data)
    print("CSV:", settings.CSV_EXPORT); print("JSON:", settings.JSON_FILE); print("Pickle:", settings.BACKUP_FILE)

if __name__ == "__main__": demo()
