"""Shared project settings for Advanced Python Programming.
The same values keep the GUI, web app, and network demos in sync.
"""

# Paths are relative to the project root so modules run with python -m.
DB_NAME = "data/registrar.db"
LOG_FILE = "data/app.log"
ACTIVITY_FILE = "data/activity.txt"
CSV_IMPORT = "data/sample_submissions.csv"
DATE_FORMAT = "%Y-%m-%d"
# CONCEPT: Shared configuration
CSV_EXPORT = "data/export.csv"
JSON_FILE = "data/results.json"
CONFIG_FILE = "data/config.json"
BACKUP_FILE = "data/backup.pkl"
REPORT_FILE = "data/report.txt"

# Network settings are shared by the socket examples and Flask client.
HOST = "127.0.0.1"
SOCKET_PORT = 5050
FLASK_PORT = 5001

# Background work is kept slow enough to observe in a classroom demo.
BACKUP_INTERVAL = 30

# CHANGE ME: Keep test mode on until SMTP credentials are configured.
EMAIL_TEST_MODE = True
EMAIL_FROM = "you@example.com"
EMAIL_TO = "parent@example.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Optional MySQL example; SQLite remains the shared project database.
MYSQL = {"host": "localhost", "user": "root", "password": "", "database": "srm"}

# This site is intentionally built for scraping practice.
BOOKS_URL = "http://books.toscrape.com/"


def demo():
    """Display the shared endpoints used by the classroom examples."""
    print("Socket server: {}:{}".format(HOST, SOCKET_PORT))
    print("Flask API: {}:{}".format(HOST, FLASK_PORT))


if __name__ == "__main__":
    demo()
