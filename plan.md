# Student Record Manager — implementation plan

## Product scope and approach

Build the full educational Python project described in the supplied `context.md`, not only a frontend mockup. Keep its five-module, concept-by-concept package layout and running demonstrations, and make the Flask portal a polished, responsive student-management experience. The SQLite-backed CRUD layer remains shared by the Flask portal, Tkinter GUI, socket server, and API client. Seed the 10 specified students from CSV only when the database is empty. Preserve the documented routes, socket line protocol, API shapes, concept markers, boundary examples, exception messages, and manual checkpoints. The optional MySQL demo must skip cleanly when its driver/server is unavailable; email stays in test mode unless explicitly changed.

The dashboard will add a clear overview of student count, pass rate, average, and highest mark; searchable/filterable student rows; grade/pass-fail status; student detail; and accessible add, edit, and delete interactions. These are presentation and workflow improvements over the intentionally plain original templates, not a replacement for the coursework modules. No login, ORM, async architecture, or unrelated product features.

## Implementation and serving

Use Python 3.10+, Flask/Jinja templates, SQLite from the standard library, and the spec's `requests` and `beautifulsoup4` dependencies. Keep `mysql-connector-python` optional. The Flask dashboard binds only to `127.0.0.1:5001`; `
` ignores `PORT` and is accessed at `http://localhost:5001`. No managed database is required: SQLite remains the coursework implementation. Flask debug mode is enabled only for the local development server.

## Project structure

- `main.py`, `settings.py`, `requirements.txt`, `README.md`, `app.config.ts`, and the provided `context.md` — lazy demo menu, shared configuration, platform logo metadata, dependencies, and learning/source-of-truth documentation.
- `data/` — sample CSV and school/year JSON; runtime SQLite and exercise output files are created as needed.
- `m1_oop/` — Person/Student hierarchy and operator demonstrations.
- `m2_functional/` — functional tools, iterators/generators, decorators, context manager/metaclass, and scope demonstrations.
- `m3_data/` — exceptions, logging, text/CSV/JSON/pickle, SQLite CRUD, and optional MySQL.
- `m4_network/` — threading/process examples, line-based socket server/client, and requests/scraping/email examples.
- `m5_apps/` — Tkinter CRUD app, Flask pages and REST API, Jinja templates (`base`, `index`, `student`, `add`), plus `static/css/app.css`, `static/js/app.js`, and `static/brand-mark.svg` for the responsive dashboard, client-side table filtering, and favicon.
- `public/manus-routes.json` — the page-route manifest served by Flask.

Keep the educational source readable and split by concept: package modules expose `demo()`, use the specified `# CONCEPT:`, `# CHANGE ME:`, and `# ADD FIELD HERE` markers, use parameterized SQL, and keep user-facing errors friendly. Preserve the sample records and expected values (10 students; total 569; mean 56.9; highest 103/Rohan Mehta/92; three failures at pass mark 40; grace-mark total 619).

## Design direction

Three considered styles: Swiss campus editorial (0.08); quiet terminal notebook with lab-inspired rules (0.04); soft neo-brutalist registrar desk (0.06). **Choose Swiss campus editorial** for the dashboard: it supports a calm academic identity while keeping marks and statuses legible.

- **Design movement:** Swiss editorial typography and information hierarchy, adapted to a contemporary university registrar workspace.
- **Core principles:** data first; confident whitespace; obvious status and action hierarchy; responsive without sacrificing table readability.
- **Color philosophy:** warm paper and ink create a grounded academic canvas; deep evergreen signals trust and action; muted amber and red distinguish attention and failure without relying on color alone.
- **Layout paradigm:** compact left navigation on desktop, stacked mobile navigation, an aligned content rail, summary strip, and a dominant student table rather than a centered card grid.
- **Signature elements:** a custom SRM monogram/wordmark; fine ruled dividers; small uppercase section labels paired with monospaced roll numbers and marks.
- **Interaction philosophy:** visible focus, clear confirmation before destructive deletion, inline validation, explicit empty/error/success states, and keyboard-friendly form submission.
- **Animation:** restrained 140–180 ms hover/focus transitions and subtle row/notice entrance; honor `prefers-reduced-motion` and avoid motion that delays input.
- **Typography system:** Inter (or system sans-serif fallback) for interface and headings; IBM Plex Mono (or system monospace fallback) for roll numbers, marks, and compact metadata.
- **Brand essence:** an explainable student-outcomes workspace for university staff and Python learners; **clear, composed, practical**.
- **Brand voice:** direct, supportive, and specific. Examples: “A clear view of every result.” “No records match these filters.”
- **Wordmark & logo:** a compact SRM monogram built from three aligned ruled bars and a small evergreen square, paired with a restrained wordmark.
- **Signature brand color:** evergreen.
