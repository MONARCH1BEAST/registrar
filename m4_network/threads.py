"""Threads, locks, and processes for Module 4 networking practice.
Module 4 demonstrates shared work, synchronisation, and separate processes.
"""

# CHANGE ME: the counter's work amount is deliberately large enough to show a race.
COUNTER_WORK = 100000

import multiprocessing
import threading
import time

import settings
from m3_data import database
from m3_data.files import backup_pickle, get_export_data


# CONCEPT: Thread synchronization
def _pass_mark():
    """Read the single pass-mark rule used by the student model."""
    try:
        from m1_oop.student import Student
        return Student.PASS_MARK
    except ImportError:
        return 40


def auto_backup(stop_event):
    """Back up the database until the event asks this daemon to stop."""
    # The event wakes the thread early, so shutdown need not wait 30 seconds.
    while not stop_event.is_set():
        try:
            backup_pickle(get_export_data())
        except Exception as error:
            print("Backup skipped:", error)
        stop_event.wait(settings.BACKUP_INTERVAL)


# CONCEPT: Multithreading in Python
def _add_many(counter, lock, use_lock):
    """Add the configured number of times, optionally under a lock."""
    for number in range(COUNTER_WORK):
        if use_lock:
            with lock:
                value = counter[0]
                time.sleep(0)
                counter[0] = value + 1
        else:
            value = counter[0]
            time.sleep(0)
            counter[0] = value + 1


def run_counter_demo(use_lock):
    """Run two workers and return their shared counter value."""
    counter = [0]
    lock = threading.Lock()

    first = threading.Thread(target=_add_many, args=(counter, lock, use_lock))
    second = threading.Thread(target=_add_many, args=(counter, lock, use_lock))
    first.start()
    second.start()
    first.join()
    second.join()
    return counter[0]


def _highest_row(rows):
    """Return the row with the highest numeric mark, if any."""
    highest = None
    for row in rows:
        if highest is None or float(row["marks"]) > float(highest["marks"]):
            highest = row
    return highest


def _average_mark(marks, count):
    """Return the average mark, using zero for an empty database."""
    if count:
        return sum(marks) / count
    return 0


def _passed_count(marks):
    """Count marks meeting the current pass-mark rule."""
    passed = 0
    for mark in marks:
        if mark >= _pass_mark():
            passed += 1
    return passed


def _pass_percentage(passed, count):
    """Return the percentage passed, using zero for no rows."""
    if count:
        return passed * 100 / count
    return 0


def _highest_text(highest):
    """Format the highest student's name and mark for the report."""
    if highest is None:
        return "None"
    return "%s (%s)" % (highest["name"], highest["marks"])


def _report_values(rows):
    """Calculate the values used by the text report."""
    marks = [float(row["marks"]) for row in rows]
    count = len(marks)
    average = _average_mark(marks, count)
    highest = _highest_row(rows)
    passed = _passed_count(marks)
    percentage = _pass_percentage(passed, count)
    highest_text = _highest_text(highest)
    return count, average, highest_text, percentage


def _write_report(count, average, highest_text, percentage):
    """Write calculated report values using the existing format."""
    with open(settings.REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("Count: %d\n" % count)
        report.write("Average: %.2f\n" % average)
        report.write("Highest: %s\n" % highest_text)
        report.write("Pass percentage: %.2f%%\n" % percentage)


def build_report():
    """Write a small summary report from the shared student database."""
    rows = database.get_all_students()
    values = _report_values(rows)
    _write_report(*values)


def _start_report_process():
    """Run report creation in a separate process and wait for it."""
    process = multiprocessing.Process(target=build_report)
    process.start()
    process.join()


def demo():
    """Show a daemon backup, a race, a locked counter, and a report process."""
    database.create_table()
    stop_event = threading.Event()
    backup_thread = threading.Thread(target=auto_backup, args=(stop_event,))
    backup_thread.daemon = True
    backup_thread.start()
    stop_event.set()
    backup_thread.join(timeout=2)
    without_lock = run_counter_demo(False)
    with_lock = run_counter_demo(True)
    print("Counter without lock:", without_lock)
    print("Counter with lock:", with_lock)
    _start_report_process()
    print("Report written to", settings.REPORT_FILE)


if __name__ == "__main__":
    # CONCEPT: Processes; creation is reached only from this Windows-safe entry.
    demo()
