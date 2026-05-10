# Campus Shuttle Backend — Updated TODO and Completion Checklist

## Current Backend Starter Status

This backend starter has been created with the core architecture needed for the MVP.

The focus is not the admin dashboard yet. The focus is the real shuttle system:

```txt
Trip start
GPS ingestion
Redis live state
PostgreSQL history
ETA calculation
Next-stop override
Student live shuttle endpoint
Stale/offline detection
```

---

# Completed in This Backend Starter

## Phase 1 — Backend Foundation

- [x] Created FastAPI backend structure
- [x] Added API versioning with `/api/v1`
- [x] Added app configuration using environment variables
- [x] Added PostgreSQL async database setup
- [x] Added Redis client setup
- [x] Added Dockerfile
- [x] Added Docker Compose with PostgreSQL/PostGIS, Redis, and API service
- [x] Added CORS configuration
- [x] Added health check endpoint
- [x] Added project README
- [x] Added requirements.txt

Status: **Mostly complete**

---

## Phase 2 — Database Models

- [x] Created `users` model
- [x] Created `drivers` model
- [x] Created `shuttles` model
- [x] Created `stops` model
- [x] Created `routes` model
- [x] Created `route_stops` model
- [x] Created `trips` model
- [x] Created `location_pings` model
- [x] Created `subscriptions` model
- [x] Created `timetable_entries` model
- [x] Created `announcements` model
- [x] Added model relationships where needed
- [x] Added status/role check constraints
- [x] Added Alembic configuration

Status: **Core model layer complete**

Remaining:

- [ ] Generate first Alembic migration
- [ ] Run migration against local PostgreSQL
- [ ] Add optional PostGIS geography columns later if needed
- [ ] Add production indexes after testing query patterns

---

## Phase 3 — Authentication and Roles

- [x] Added password hashing
- [x] Added JWT token creation
- [x] Added JWT token decoding
- [x] Added register endpoint
- [x] Added login endpoint
- [x] Added `/auth/me`
- [x] Added current user dependency
- [x] Added role-based permission helper
- [x] Protected driver endpoints
- [x] Protected setup/admin-style write endpoints

Status: **MVP authentication complete**

Remaining:

- [ ] Add refresh tokens if needed
- [ ] Add password reset later
- [ ] Add school email restriction if required
- [ ] Add stricter admin user creation process before production

---

## Phase 4 — Basic Setup APIs

- [x] Added stop list/create/update endpoints
- [x] Added route list/create endpoints
- [x] Added route-stop add endpoint
- [x] Added shuttle list/create/update endpoints
- [x] Added timetable list/create endpoints

Status: **Lightweight setup APIs complete**

Remaining:

- [ ] Add route stop reorder endpoint
- [ ] Add soft delete/disable endpoints
- [ ] Add driver creation endpoint
- [ ] Add admin dashboard later

---

## Phase 5 — Driver Trip Flow

- [x] Added start trip endpoint
- [x] Validates driver profile
- [x] Validates route
- [x] Validates shuttle
- [x] Prevents starting a second active trip for same shuttle
- [x] Selects initial next stop automatically from route if not provided
- [x] Stores active trip in PostgreSQL
- [x] Stores active trip state in Redis
- [x] Updates shuttle status to active
- [x] Added end trip endpoint
- [x] Updates trip status to completed
- [x] Removes trip from active Redis set
- [x] Updates shuttle status to inactive

Status: **Core trip flow complete**

Remaining:

- [ ] Add stronger driver-shuttle assignment validation
- [ ] Add trip event log table/service
- [ ] Add admin trip override later

---

## Phase 6 — GPS Location Ingestion

- [x] Added driver GPS ping endpoint
- [x] Validates trip exists
- [x] Validates trip belongs to driver
- [x] Validates trip is active/delayed/paused/offline
- [x] Stores GPS ping in PostgreSQL
- [x] Stores latest live state in Redis
- [x] Updates last ping timestamp
- [x] Returns live trip response to driver
- [x] Restores offline trip back to active when GPS resumes

Status: **Core GPS ingestion complete**

Remaining:

- [ ] Add rate limiting per driver/device
- [ ] Add duplicate GPS ping filtering
- [ ] Add noisy GPS filtering
- [ ] Add background worker for stale detection

---

## Phase 7 — ETA and Speed Algorithm

- [x] Added Haversine distance algorithm
- [x] Added speed calculation from two GPS points
- [x] Added phone speed validation
- [x] Added speed plausibility checks
- [x] Added speed smoothing with recent samples
- [x] Added default average speed fallback
- [x] Added ETA calculation
- [x] Added distance-to-next-stop in response

Status: **MVP ETA algorithm complete**

Remaining:

- [ ] Add geofence arrival detection
- [ ] Add road-distance ETA using OSRM/Mapbox/Google later
- [ ] Add stop dwell-time prediction later
- [ ] Add historical ETA tuning later

---

## Phase 8 — Driver Next-Stop Override

- [x] Added change next stop endpoint
- [x] Validates stop exists
- [x] Validates driver owns trip
- [x] Updates `trips.next_stop_id`
- [x] Updates Redis live state with new next stop
- [x] Student endpoint will show updated next stop

Status: **MVP next-stop override complete**

Remaining:

- [ ] Recalculate ETA immediately using latest live GPS after next-stop change
- [ ] Add trip event log for next-stop changes
- [ ] Notify students if their stop is affected

---

## Phase 9 — Student Live Shuttle APIs

- [x] Added active shuttles endpoint
- [x] Added live trip endpoint
- [x] Reads live state from Redis
- [x] Falls back to active trips from PostgreSQL if Redis active set is empty
- [x] Returns shuttle location
- [x] Returns status
- [x] Returns next stop
- [x] Returns ETA
- [x] Returns stale/offline flags
- [x] Returns last updated timestamp

Status: **Core student live API complete**

Remaining:

- [ ] Add timetable grouped by route/day
- [ ] Add route detail endpoint with ordered stops
- [ ] Add public announcements endpoint

---

## Phase 10 — Stale and Offline Detection

- [x] Added stale flag calculation
- [x] Added offline flag calculation
- [x] Added Redis live-state stale checks
- [x] Added database status update to offline when needed

Status: **Basic stale/offline logic complete**

Remaining:

- [ ] Add scheduled background stale checker
- [ ] Add admin notification when shuttle goes offline
- [ ] Add driver reconnect/resume UX support later

---

# Current Stage of the Project

The backend is now at:

```txt
Backend MVP Foundation + Core Live Tracking Logic
```

You are currently between:

```txt
Phase 7: ETA calculation
and
Phase 9: Student live shuttle APIs
```

The backend code now has enough foundation to begin connecting the Flutter driver app and student app.

---

# What Should Be Done Next

## Immediate Next Step 1 — Run Backend Locally

- [ ] Copy `.env.example` to `.env`
- [ ] Run Docker Compose
- [ ] Generate initial migration
- [ ] Run Alembic migration
- [ ] Confirm `/api/v1/health` works

Commands:

```bash
cd backend
cp .env.example .env
docker compose up --build
docker compose exec api alembic revision --autogenerate -m "initial schema"
docker compose exec api alembic upgrade head
```

---

## Immediate Next Step 2 — Add Seed Data

- [ ] Create admin user
- [ ] Create driver user
- [ ] Create driver profile
- [ ] Create test shuttle
- [ ] Create Main Campus stop
- [ ] Create Off-Campus stop
- [ ] Create Sub-Campus stop
- [ ] Create test route
- [ ] Add ordered route stops

---

## Immediate Next Step 3 — Test Core Flow With API Client

- [ ] Register/login driver
- [ ] Start trip
- [ ] Send GPS ping
- [ ] Read `/student/shuttles/active`
- [ ] Change next stop
- [ ] Send another GPS ping
- [ ] End trip

---

## Immediate Next Step 4 — Build Flutter Driver App

- [ ] Login screen
- [ ] Start trip screen
- [ ] Active trip screen
- [ ] GPS permission
- [ ] GPS ping loop
- [ ] Change next stop
- [ ] End trip

---

## Immediate Next Step 5 — Build Flutter Student App

- [ ] Live map screen
- [ ] Active shuttle API call
- [ ] Shuttle marker
- [ ] Stop markers
- [ ] ETA card
- [ ] Next stop card
- [ ] Stale/offline warning

---

# Files Created

## Core Backend

- [x] `app/main.py`
- [x] `app/core/config.py`
- [x] `app/core/security.py`
- [x] `app/core/constants.py`
- [x] `app/core/permissions.py`
- [x] `app/db/session.py`
- [x] `app/db/redis.py`
- [x] `app/db/base.py`

## Models

- [x] `app/models/user.py`
- [x] `app/models/driver.py`
- [x] `app/models/shuttle.py`
- [x] `app/models/stop.py`
- [x] `app/models/route.py`
- [x] `app/models/route_stop.py`
- [x] `app/models/trip.py`
- [x] `app/models/location_ping.py`
- [x] `app/models/subscription.py`
- [x] `app/models/timetable.py`
- [x] `app/models/announcement.py`

## Schemas

- [x] `app/schemas/auth.py`
- [x] `app/schemas/user.py`
- [x] `app/schemas/stop.py`
- [x] `app/schemas/route.py`
- [x] `app/schemas/shuttle.py`
- [x] `app/schemas/driver.py`
- [x] `app/schemas/trip.py`
- [x] `app/schemas/location.py`
- [x] `app/schemas/timetable.py`

## Services

- [x] `app/services/auth_service.py`
- [x] `app/services/trip_service.py`
- [x] `app/services/location_service.py`
- [x] `app/services/eta_service.py`
- [x] `app/services/live_state_service.py`
- [x] `app/services/stale_detection_service.py`
- [x] `app/services/notification_service.py`

## Repositories

- [x] `app/repositories/user_repository.py`
- [x] `app/repositories/driver_repository.py`
- [x] `app/repositories/shuttle_repository.py`
- [x] `app/repositories/stop_repository.py`
- [x] `app/repositories/route_repository.py`
- [x] `app/repositories/trip_repository.py`
- [x] `app/repositories/location_repository.py`
- [x] `app/repositories/timetable_repository.py`

## API Endpoints

- [x] `app/api/v1/endpoints/auth.py`
- [x] `app/api/v1/endpoints/driver.py`
- [x] `app/api/v1/endpoints/student.py`
- [x] `app/api/v1/endpoints/stops.py`
- [x] `app/api/v1/endpoints/routes.py`
- [x] `app/api/v1/endpoints/shuttles.py`
- [x] `app/api/v1/endpoints/timetable.py`
- [x] `app/api/v1/endpoints/health.py`

---

# Honest Limitations

This is a strong backend starter, but it is not yet a finished production backend.

Important remaining work:

- Generate and test actual Alembic migration
- Add seed data
- Add driver profile creation endpoint or seed script
- Add real Firebase Cloud Messaging implementation
- Add rate limiting
- Add background stale checker
- Add road-based ETA later
- Add geofencing later
- Add integration tests with a real test database
