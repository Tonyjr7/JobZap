# EXTENSION

A small Python project that fetches and extracts data, persists jobs to a database, and provides migration support via Alembic. The codebase includes services for interacting with Discord, an extractor, and a simple fetcher route.

## Features

- Fetch data from external sources (see `route/fetcher.py`).
- Extract and process data (see `services/extractor.py`).
- Discord integration helper (see `services/discord.py`).
- SQLAlchemy models and database utilities (in `database/`).
- Database migrations managed with Alembic (in `migrations/`).

## Requirements

- Python 3.10+ recommended
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment

Create a `.env` file in the project root or export environment variables. Common variables used by the project:

- `DATABASE_URL` — the SQLAlchemy database URL (e.g. `postgresql://user:pass@localhost/dbname`).
- Any Discord-related tokens or API keys consumed by `services/discord.py`.
- See `settings.py` for additional configuration keys.

## Database & Migrations

The project uses SQLAlchemy and Alembic. Typical workflow:

```bash
# Create migrations (after modifying models)
alembic revision --autogenerate -m "describe change"

# Apply migrations
alembic upgrade head
```

Alembic configuration is stored in `alembic.ini` and the migration scripts live under `migrations/versions`.

## Running the project

Run the main application entrypoint:

```bash
python main.py
```

For ASGI serving (if `main.py` exposes a FastAPI app), run with Uvicorn:

```bash
uvicorn main:app --reload
```

Adjust the command according to how `main.py` exposes the app or entrypoint.

## Project Structure

- `main.py` — application entrypoint.
- `settings.py` — configuration and environment handling.
- `database/` — SQLAlchemy engine, session, and model definitions.
  - `database.py`, `base.py`, `models/job.py`.
- `services/` — business logic and integrations (`discord.py`, `extractor.py`).
- `route/` — route handlers or fetcher utilities (`fetcher.py`).
- `migrations/` — Alembic migration scripts and env configuration.
- `requirements.txt` — pinned dependencies.

## Contributing

1. Create an issue describing the change.
2. Branch from `main` and open a PR with a clear title and description.
3. Add or update migrations when changing models.

## License

This repository does not include a LICENSE file. Add one if you intend to publish.

---
