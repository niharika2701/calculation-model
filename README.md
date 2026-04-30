# Module 11 — Calculation Model, Pydantic Schemas & Factory Pattern

**IS 601 | Python for Web API | NJIT**

Builds on Module 10 by adding a `Calculation` SQLAlchemy model, Pydantic
validation schemas, a factory pattern for arithmetic operations, and full
unit + integration test coverage.

---

## Docker Hub

Image: `niharika2701/module11-calculations-api:latest`

```bash
docker pull niharika2701/module11-calculations-api:latest
```

🔗 [Docker Hub Repository](https://hub.docker.com/r/niharika2701/module11-calculations-api)

---

## Project Structure

Module 11/
├── app/
│   ├── calculations.py     # OperationType enum + CalculationFactory
│   ├── models.py           # User + Calculation SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas (UserCreate, UserRead,
│   │                       #   CalculationCreate, CalculationRead)
│   ├── database.py         # SQLAlchemy engine and session
│   └── auth.py             # Password hashing
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_schemas.py
│   ├── test_users.py
│   ├── test_calculations_unit.py        # Factory + schema unit tests
│   └── test_calculations_integration.py # DB integration tests
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions — test + Docker Hub deploy
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt

---

## How to Run Tests Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run all tests

```bash
python -m pytest tests/ -v
```

### 3. Run only calculation tests

```bash
# Unit tests (no database needed)
python -m pytest tests/test_calculations_unit.py -v

# Integration tests (uses SQLite locally)
python -m pytest tests/test_calculations_integration.py -v
```

---

## What's New in Module 11

### OperationType Enum
Defined in `app/calculations.py`. Valid values: `Add`, `Sub`, `Multiply`, `Divide`.
Inherits from `str` so Pydantic serialises these as plain strings in JSON.

### CalculationFactory
Maps each `OperationType` to a lambda function.
Adding a new operation = one new dictionary entry. No existing code changes.
This is the **Open/Closed Principle** in practice.

### Calculation Model
SQLAlchemy model in `app/models.py` with fields:
`id`, `a`, `b`, `type`, `result`, `user_id` (nullable FK → users), `created_at`.

### Pydantic Schemas
- `CalculationCreate` — validates input, rejects invalid types and division by zero
- `CalculationRead` — serialises output including computed result

---

## CI/CD Pipeline

GitHub Actions (`.github/workflows/ci.yml`) runs on every push:

1. **Test job** — spins up PostgreSQL 16, runs all user + calculation tests
2. **Deploy job** — builds Docker image and pushes to Docker Hub on success