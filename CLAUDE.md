# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run

```
pip install -r requirements.txt
export NOTION_TOKEN=...           # Notion integration token
export NOTION_DATABASE_ID=...     # ID of the tasks database
python backend/app.py             # Flask debug server on http://localhost:5050
```

The frontend is served by Flask at `/` (no separate dev server, no build step). There are no tests or linters configured.

## Architecture

Two-tier app where **Notion is the database**:

- `backend/app.py` — Flask + flask-cors + notion-client. Serves `frontend/index.html` at `/` and exposes `GET/POST/PUT/DELETE /tasks` that proxy to the Notion database identified by `NOTION_DATABASE_ID`.
- `frontend/index.html` — single file containing all markup, Tailwind (CDN), Flatpickr (CDN), and the JS that fetches `/tasks` and renders task cards into time-bucketed columns plus an ASAP priority bar.

There is no client-side framework, no bundler, and no local persistence — every task read/write is a Notion API round-trip.

### Notion schema (load-bearing)

The backend reads/writes these exact property names on the Notion database. Renaming any of them in Notion will break the endpoints:

- `Title` (title)
- `Due Date` (date)
- `Description` (rich_text)
- `Priority` (select: `Low`, `Medium`, `ASAP`)
- `Status` (select: `to-do`, ...)

### Frontend bucketing

`displayTasks()` in `frontend/index.html` groups tasks: `priority === "ASAP"` → priority bar; otherwise placed into Past / Last Week / This Week / Next Week / Future based on `dueDate` against Monday-anchored week boundaries.

## Gotchas

- `POST /tasks` returns `{"status": "success"}` and does **not** include the new Notion page id, so the frontend stores `id: null` for new tasks until the next `fetchTasks()`. Editing/deleting a newly-created task before reload won't work — fix this by returning the page id from the create handler if you touch that path.
- `PUT /tasks/<id>` unconditionally resets `Status` to `"to-do"`.
- "Mark Complete" calls `DELETE`, which archives the Notion page (`archived=True`). There is no real completed state.
- `data/tasks.json` is sample data, not used by the running app — don't assume it's a fallback or cache.
