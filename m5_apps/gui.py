"""Tkinter master-detail registrar for assignments and submissions."""
import sqlite3, tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
import settings
from m3_data import database
from m3_data.logger import setup_logging

# CONCEPT: Tkinter widgets and event-driven CRUD
class App:
    def __init__(self, root):
        self.root = root; root.title("Student Hub Registrar"); root.geometry("920x520")
        database.create_table(); pane = ttk.Panedwindow(root, orient="horizontal"); pane.pack(fill="both", expand=True, padx=12, pady=12)
        left, right = ttk.Frame(pane, padding=8), ttk.Frame(pane, padding=8); pane.add(left, weight=1); pane.add(right, weight=2)
        ttk.Label(left, text="Assignments").pack(anchor="w"); ttk.Label(right, text="Submissions").pack(anchor="w")
        self.assignments = self._tree(left, ("ID", "Title"), (60, 220)); self.submissions = self._tree(right, ("Roll", "Name", "Marks", "Date"), (70, 150, 80, 110))
        self.assignments.bind("<<TreeviewSelect>>", self._select)
        ttk.Button(left, text="Add Assignment", command=self.add_assignment).pack(fill="x", pady=8)
        bar = ttk.Frame(right); bar.pack(fill="x", pady=8)
        for label, fn in (("Add Submission", self.add_submission), ("Delete Submission", self.delete_submission)):
            ttk.Button(bar, text=label, command=fn).pack(side="left", padx=4)
        self.status = tk.StringVar(value="Select an assignment."); ttk.Label(root, textvariable=self.status, padding=8).pack(fill="x"); self.refresh()
    def _tree(self, parent, columns, widths):
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col, width in zip(columns, widths): tree.heading(col, text=col); tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True); return tree
    def refresh(self):
        selected = self.assignments.selection()
        for item in self.assignments.get_children(): self.assignments.delete(item)
        for row in database.get_all_assignments(): self.assignments.insert("", "end", iid=str(row["id"]), values=(row["id"], row["title"]))
        if selected and self.assignments.exists(selected[0]): self.assignments.selection_set(selected[0]); self._load(int(selected[0]))
        else: self._load(None)
    def _load(self, aid):
        for item in self.submissions.get_children(): self.submissions.delete(item)
        if aid is not None:
            for row in database.get_submissions_for_assignment(aid):
                self.submissions.insert("", "end", iid=str(row["id"]), values=(row["roll"], row["name"], row["marks"], row["submitted_on"]))
        self.status.set("Select an assignment." if aid is None else "Submissions: {}".format(len(self.submissions.get_children())))
    def _select(self, _event=None):
        if self.assignments.selection(): self._load(int(self.assignments.selection()[0]))
    def _popup(self, title, fields, save):
        win = tk.Toplevel(self.root); win.title(title); win.transient(self.root); win.grab_set(); inputs = {}
        for i, (key, label, values) in enumerate(fields):
            ttk.Label(win, text=label).grid(row=i, column=0, padx=10, pady=6, sticky="w")
            widget = ttk.Combobox(win, values=values, state="readonly") if isinstance(values, list) else ttk.Entry(win, width=28)
            if isinstance(values, str): widget.insert(0, values)
            widget.grid(row=i, column=1, padx=10, pady=6); inputs[key] = widget
        def submit():
            try: save({key: widget.get().strip() for key, widget in inputs.items()})
            except (ValueError, sqlite3.IntegrityError) as error: messagebox.showerror(title, str(error), parent=win); return
            win.destroy(); self.refresh()
        ttk.Button(win, text="Save", command=submit).grid(row=len(fields), column=1, padx=10, pady=10, sticky="e")
    def _selected(self, tree, label):
        if not tree.selection(): raise ValueError("Select a {} first.".format(label))
        return int(tree.selection()[0])
    def add_assignment(self):
        self._popup("Add Assignment", [("title", "Title", ""), ("max", "Maximum marks", "100"), ("due", "Due date", date.today().strftime(settings.DATE_FORMAT))],
                    lambda d: database.add_assignment(d["title"], float(d["max"]), d["due"]))
    def add_submission(self):
        try: aid = self._selected(self.assignments, "assignment")
        except ValueError as error: messagebox.showerror("Add Submission", str(error), parent=self.root); return
        students = database.get_all_students(); choices = ["{} | {}".format(s["roll"], s["name"]) for s in students]
        def save(data):
            roll = data["student"].split(" | ", 1)[0]; marks = float(data["marks"])
            if not 0 <= marks <= database.get_assignment(aid)["max_marks"]: raise ValueError("Marks exceed the assignment maximum.")
            database.add_submission(aid, roll, marks, data["date"])
        self._popup("Add Submission", [("student", "Student", choices), ("marks", "Marks", ""), ("date", "Submitted on", date.today().strftime(settings.DATE_FORMAT))], save)
    def delete_submission(self):
        try: sid = self._selected(self.submissions, "submission")
        except ValueError as error: messagebox.showerror("Delete Submission", str(error), parent=self.root); return
        if messagebox.askyesno("Delete Submission", "Delete selected submission?", parent=self.root): database.delete_submission(sid); self.refresh()

def main(): setup_logging(); root = tk.Tk(); App(root); root.mainloop()
def demo(): main()
if __name__ == "__main__": demo()
