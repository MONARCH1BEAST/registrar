# Student Hub - Academic Registrar

Student Hub is a small academic registrar application for managing batches, students, assignments, and student submissions. It provides both a Flask web interface and a Tkinter desktop application backed by a shared SQLite database.

## Tech Stack

- Python 3.10+
- Flask
- SQLite
- Tkinter
- Vanilla JavaScript and CSS

## Setup

Run these commands from the project root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m m3_data.database
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m m3_data.database
```

The database command initializes the SQLite schema at `data/registrar.db`. The `data/` directory must be available from the project root. Tkinter is included with many Python installations; on some Linux distributions it must be installed separately through the system package manager.

## Run the Applications

Start the Flask web app:

```bash
python -m m5_apps.web
```

Open [http://localhost:5001](http://localhost:5001) in a browser.

Start the Tkinter desktop app in a separate terminal:

```bash
python -m m5_apps.gui
```

## Data and Configuration

Both applications use the same local SQLite database, configured by `DB_NAME` in `settings.py`. The `.gitignore` keeps local SQLite databases, log files, Python bytecode, virtual environments, and environment-variable files out of Git while leaving the `data/` directory available to the project.

The Flask development server is intended for local use. Review the application's security and deployment requirements before making it available beyond your local machine.
