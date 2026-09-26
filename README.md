# FastAPI ToDo List

A simple REST API for managing tasks and categories, built with FastAPI, SQLAlchemy (async) and PostgreSQL.

## Stack

- Python 3.14
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- Alembic for migrations
- PostgreSQL 18
- uv for dependency management
- Docker / docker-compose

## Project structure

```
app/
├── api/
│   ├── dependencies/   # FastAPI dependencies (DB session, service injection)
│   └── routers/        # HTTP routes
├── core/                # config, logging, middleware, exceptions
├── db/                  # session setup
├── models/               # SQLAlchemy ORM models
├── repositories/         # DB access layer
├── schemas/               # Pydantic schemas
└── services/               # business logic
```

Standard layered structure: router → service → repository → model.

## Running locally

### With Docker (recommended)

1. Copy `.env.example` to `.env` and fill in the values:

```
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=todo
CORS_ORIGINS=["http://localhost:3000"]
```

2. Run:

```
docker compose up --build
```

The API will be available at `http://localhost:8080`. Postgres is exposed on port `5432`.

3. Apply migrations (from inside the container or locally with the same `.env`):

```
docker compose exec backend uv run alembic upgrade head
```

### Without Docker

Requires a local PostgreSQL instance and `uv` installed.

```
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

## Endpoints

### Tasks — `/tasks`

| Method | Path          | Description       |
|--------|---------------|-------------------|
| GET    | `/tasks`      | List all tasks    |
| POST   | `/tasks`      | Create a task      |
| PATCH  | `/tasks/{id}` | Update a task      |
| DELETE | `/tasks/{id}` | Delete a task      |

### Categories — `/categories`

| Method | Path              | Description         |
|--------|-------------------|----------------------|
| GET    | `/categories`      | List all categories  |
| POST   | `/categories`      | Create a category    |
| PATCH  | `/categories/{id}` | Update a category    |
| DELETE | `/categories/{id}` | Delete a category    |

Interactive docs (Swagger) are available at `/docs` once the app is running.

## Development

The project uses `ruff` for linting/formatting and `mypy` (strict) for type checking, wired up through pre-commit.

```
uv sync --group dev
uv run pre-commit install
```

Run checks manually:

```
uv run ruff check .
uv run ruff format .
uv run mypy .
```

## Migrations

New migration after changing models:

```
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
```

## Notes

- CORS origins are configurable via `CORS_ORIGINS` in `.env`.
- Every request gets a request number and is logged (see `app/core/middleware.py`).
- Categories aren't yet linked to tasks at the model level — that's the obvious next step.
