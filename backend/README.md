# Campus Shuttle Tracking Backend

FastAPI backend starter for the Campus Shuttle Tracking System.

This backend focuses on the core system:

```txt
Driver starts trip
↓
Driver phone sends GPS
↓
Backend stores latest live state in Redis
↓
Backend stores permanent trip/location history in PostgreSQL
↓
Student app reads live shuttle state, ETA, next stop, and status
```

## Stack

- FastAPI
- PostgreSQL + PostGIS image for local development
- SQLAlchemy async
- Alembic migrations
- Redis
- JWT authentication
- Pydantic v2
- Docker Compose

## Local Setup

```bash
cd backend
cp .env.example .env
docker compose up --build
```

In another terminal:

```bash
docker compose exec api alembic upgrade head
```

The API will run at:

```txt
http://localhost:8000
```

Docs:

```txt
http://localhost:8000/docs
```

## Main API Areas

```txt
/api/v1/auth
/api/v1/driver
/api/v1/student
/api/v1/stops
/api/v1/routes
/api/v1/shuttles
/api/v1/timetable
/api/v1/health
```

## Core MVP Flow

1. Create stops.
2. Create a route.
3. Add ordered stops to route.
4. Create shuttle.
5. Create driver user and driver profile.
6. Driver starts trip.
7. Driver sends GPS pings.
8. Student app reads active shuttle live state.
9. Driver changes next stop if needed.
10. Driver ends trip.

## Important Design Decision

Redis stores the latest live shuttle state.

PostgreSQL stores permanent records and history.

The student app should read clean live state from the API, not raw historical GPS rows.
