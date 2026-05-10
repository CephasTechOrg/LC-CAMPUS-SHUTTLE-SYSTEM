# Campus Shuttle Tracking System — TODO and Build Plan

## Purpose

This file breaks the system into clear development phases with checklists. The goal is to build the system step by step without overcomplicating the MVP.

The MVP should prove this flow first:

```txt
Driver starts trip
↓
Phone sends GPS
↓
Backend receives location
↓
Redis stores latest location
↓
PostgreSQL stores trip history
↓
Student app shows shuttle on map
↓
ETA updates based on next stop
```

---

# Phase 0 — Planning and Setup

## Goals

Prepare the project structure, development environment, and core technical decisions.

## Checklist

- [ ] Choose project name.
- [ ] Create GitHub repository.
- [ ] Create backend folder.
- [ ] Create mobile folder.
- [ ] Create admin-dashboard folder.
- [ ] Create docs folder.
- [ ] Add documentation files.
- [ ] Decide environment variable structure.
- [ ] Decide local development database setup.
- [ ] Set up Docker Compose for local PostgreSQL and Redis.
- [ ] Decide map provider for MVP.
- [ ] Decide whether student and driver apps will be one app with roles or separate apps.

## Recommended Decision

Use separate apps or separate app modes:

```txt
Student App = public tracking and notifications
Driver App = trip control and GPS tracking
Admin Dashboard = operations management
```

---

# Phase 1 — Backend Foundation

## Goals

Build the FastAPI backend foundation.

## Checklist

- [ ] Initialize FastAPI project.
- [ ] Set up project structure.
- [ ] Set up environment variables.
- [ ] Set up PostgreSQL connection.
- [ ] Set up Redis connection.
- [ ] Set up SQLAlchemy or SQLModel.
- [ ] Set up Alembic migrations.
- [ ] Add health check endpoint.
- [ ] Add error handling structure.
- [ ] Add CORS settings.
- [ ] Add API versioning with `/api/v1`.

## Suggested Backend Folders

```txt
backend/app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── utils/
└── main.py
```

## Completion Criteria

- [ ] Backend runs locally.
- [ ] Database connects successfully.
- [ ] Redis connects successfully.
- [ ] Health endpoint returns success.
- [ ] Migrations run successfully.

---

# Phase 2 — Database Models

## Goals

Create the main database schema.

## Checklist

- [ ] Create users table.
- [ ] Create stops table.
- [ ] Create routes table.
- [ ] Create route_stops table.
- [ ] Create shuttles table.
- [ ] Create drivers table.
- [ ] Create trips table.
- [ ] Create location_pings table.
- [ ] Create subscriptions table.
- [ ] Create timetable_entries table.
- [ ] Create announcements table.
- [ ] Add indexes.
- [ ] Add foreign key constraints.
- [ ] Add enum/check constraints for statuses and roles.
- [ ] Run migrations.
- [ ] Seed initial test data.

## Seed Data

Create test data for:

- [ ] Main Campus stop.
- [ ] Off-Campus Housing stop.
- [ ] Sub-Campus stop.
- [ ] One route.
- [ ] One shuttle.
- [ ] One driver.
- [ ] One admin.

## Completion Criteria

- [ ] Database tables exist.
- [ ] Test route and stops exist.
- [ ] A trip can reference route, shuttle, driver, and stops.

---

# Phase 3 — Authentication and Roles

## Goals

Add authentication for students, drivers, and admins.

## Checklist

- [ ] Create registration endpoint if needed.
- [ ] Create login endpoint.
- [ ] Hash passwords.
- [ ] Generate JWT access tokens.
- [ ] Add role-based authorization.
- [ ] Add current user dependency.
- [ ] Protect driver endpoints.
- [ ] Protect admin endpoints.
- [ ] Keep public student shuttle tracking endpoints open.

## Access Rules

```txt
Public:
- View active shuttle
- View timetable
- View routes/stops

Student login required:
- Preferred stop
- Notifications
- Feedback

Driver login required:
- Start trip
- Send GPS
- Change next stop
- Report delay
- Cancel trip
- End trip

Admin login required:
- Manage system data
```

## Completion Criteria

- [ ] Drivers can access driver endpoints.
- [ ] Admins can access admin endpoints.
- [ ] Public users can view shuttle data without login.

---

# Phase 4 — Admin Core APIs

## Goals

Build admin APIs for system setup.

## Checklist

## Stops

- [ ] Create stop.
- [ ] Get stops.
- [ ] Get single stop.
- [ ] Update stop.
- [ ] Disable/delete stop.

## Routes

- [ ] Create route.
- [ ] Get routes.
- [ ] Get single route.
- [ ] Update route.
- [ ] Disable/delete route.

## Route Stops

- [ ] Add stop to route.
- [ ] Reorder route stops.
- [ ] Remove stop from route.

## Shuttles

- [ ] Create shuttle.
- [ ] Get shuttles.
- [ ] Update shuttle.
- [ ] Set shuttle status.

## Drivers

- [ ] Create driver profile.
- [ ] Assign driver to shuttle.
- [ ] Get drivers.
- [ ] Update driver.

## Timetable

- [ ] Create timetable entry.
- [ ] Get timetable.
- [ ] Update timetable entry.
- [ ] Disable timetable entry.

## Completion Criteria

- [ ] Admin can set up route, stops, driver, shuttle, and timetable from APIs.

---

# Phase 5 — Driver Trip Flow

## Goals

Allow a driver to start and manage a shuttle trip.

## Checklist

- [ ] Create start trip endpoint.
- [ ] Validate driver identity.
- [ ] Validate route exists.
- [ ] Validate shuttle exists.
- [ ] Set trip status to active.
- [ ] Set actual_start_time.
- [ ] Set initial next_stop_id.
- [ ] Store active trip in PostgreSQL.
- [ ] Store active trip state in Redis.
- [ ] Create end trip endpoint.
- [ ] Set actual_end_time.
- [ ] Set status to completed.
- [ ] Clear active trip from Redis or mark completed.
- [ ] Update shuttle status.

## Driver APIs

```txt
POST   /api/v1/driver/trips/start
POST   /api/v1/driver/trips/{trip_id}/end
```

## Completion Criteria

- [ ] Driver can start a trip.
- [ ] Driver can end a trip.
- [ ] Active trip is visible in backend.

---

# Phase 6 — GPS Location Ingestion

## Goals

Receive and process live GPS pings from the driver app.

## Checklist

- [ ] Create location ping endpoint.
- [ ] Validate trip is active.
- [ ] Validate driver is assigned to trip.
- [ ] Validate latitude and longitude.
- [ ] Store latest location in Redis.
- [ ] Store historical location in PostgreSQL.
- [ ] Calculate speed if possible.
- [ ] Calculate ETA to next stop.
- [ ] Update last_ping_at.
- [ ] Return live trip state.

## API

```txt
POST /api/v1/driver/trips/{trip_id}/location
```

## Example Request

```json
{
  "latitude": 35.12345,
  "longitude": -80.12345,
  "speed_mph": 18.4,
  "heading": 90
}
```

## Completion Criteria

- [ ] Backend receives GPS pings.
- [ ] Redis stores latest live location.
- [ ] PostgreSQL stores historical pings.
- [ ] ETA is calculated.

---

# Phase 7 — ETA Calculation

## Goals

Calculate the estimated time from the shuttle’s current location to the next stop.

## Checklist

- [ ] Implement Haversine distance formula.
- [ ] Fetch next stop coordinates.
- [ ] Use default average speed.
- [ ] Calculate ETA in minutes.
- [ ] Handle zero speed.
- [ ] Handle missing next stop.
- [ ] Handle stale location.
- [ ] Add speed smoothing from recent GPS pings.
- [ ] Store ETA in Redis live state.

## MVP Formula

```txt
ETA = distance_to_next_stop / average_speed
```

## Speed Rules

- [ ] Use phone-provided speed when reliable.
- [ ] Otherwise calculate speed from recent points.
- [ ] Average last 5–10 speed samples.
- [ ] Fall back to default speed if speed is missing or unstable.

## Completion Criteria

- [ ] ETA is returned in student live shuttle endpoint.
- [ ] ETA updates when the shuttle moves.
- [ ] ETA updates when driver changes next stop.

---

# Phase 8 — Driver Next-Stop Override

## Goals

Allow the driver to change the next stop at any time.

## Checklist

- [ ] Create change next stop endpoint.
- [ ] Validate stop exists.
- [ ] Validate trip is active.
- [ ] Update trips.next_stop_id.
- [ ] Update Redis live state.
- [ ] Recalculate ETA.
- [ ] Create trip event log.
- [ ] Notify students if needed.

## API

```txt
PATCH /api/v1/driver/trips/{trip_id}/next-stop
```

## Example Request

```json
{
  "next_stop_id": "stop_uuid"
}
```

## Completion Criteria

- [ ] Driver can change next stop.
- [ ] Student app sees new next stop.
- [ ] ETA recalculates immediately.

---

# Phase 9 — Student Live Shuttle APIs

## Goals

Allow students to view live shuttle data.

## Checklist

- [ ] Create get active shuttles endpoint.
- [ ] Create get live trip endpoint.
- [ ] Return shuttle location.
- [ ] Return trip status.
- [ ] Return next stop.
- [ ] Return ETA.
- [ ] Return last updated time.
- [ ] Return stale/offline flag.
- [ ] Return route information.
- [ ] Return timetable information.

## APIs

```txt
GET /api/v1/student/shuttles/active
GET /api/v1/student/trips/{trip_id}/live
GET /api/v1/student/routes
GET /api/v1/student/timetable
```

## Example Response

```json
{
  "trip_id": "trip_uuid",
  "status": "active",
  "shuttle": {
    "id": "shuttle_uuid",
    "name": "Campus Shuttle 1"
  },
  "location": {
    "latitude": 35.12345,
    "longitude": -80.12345,
    "heading": 90
  },
  "next_stop": {
    "id": "stop_uuid",
    "name": "Off-Campus Housing",
    "latitude": 35.12888,
    "longitude": -80.12999
  },
  "eta_minutes": 7,
  "last_updated": "2026-05-09T14:32:00Z",
  "is_location_stale": false
}
```

## Completion Criteria

- [ ] Student app can read active shuttle.
- [ ] Student app can display shuttle marker.
- [ ] Student app can show ETA and next stop.

---

# Phase 10 — Student Mobile App

## Goals

Build the student-facing mobile experience.

## Checklist

- [ ] Create app project.
- [ ] Add map screen.
- [ ] Add shuttle marker.
- [ ] Add stop markers.
- [ ] Add status card.
- [ ] Add next stop display.
- [ ] Add ETA display.
- [ ] Add timetable screen.
- [ ] Add refresh/polling logic.
- [ ] Add loading and error states.
- [ ] Add no-active-shuttle state.
- [ ] Add optional login.
- [ ] Add preferred stop selection.
- [ ] Add notification settings.

## MVP Screens

- [ ] Home/live map screen.
- [ ] Timetable screen.
- [ ] Route details screen.
- [ ] Login screen.
- [ ] Notification preferences screen.

## Completion Criteria

- [ ] Student can open app and see active shuttle without logging in.
- [ ] Student can see current status, ETA, and next stop.

---

# Phase 11 — Driver Mobile App

## Goals

Build the driver-facing mobile experience.

## Checklist

- [ ] Create driver app project or driver mode.
- [ ] Add login screen.
- [ ] Add route selection.
- [ ] Add shuttle selection if needed.
- [ ] Add start trip button.
- [ ] Add active trip screen.
- [ ] Add background GPS tracking.
- [ ] Add location ping sender.
- [ ] Add change next stop feature.
- [ ] Add report delay feature.
- [ ] Add cancel trip feature.
- [ ] Add end trip feature.
- [ ] Add offline/error state.
- [ ] Add battery/location permission handling.

## Driver UX Rule

The driver app should stay simple.

The main screen should show:

- Current trip status
- Current location status
- Next stop
- Start/end trip button
- Change next stop button
- Delay/cancel controls

## Completion Criteria

- [ ] Driver can start trip.
- [ ] GPS updates are sent automatically.
- [ ] Driver can change next stop.
- [ ] Driver can end trip.

---

# Phase 12 — Notifications

## Goals

Notify students about important shuttle events.

## Checklist

- [ ] Set up Firebase Cloud Messaging.
- [ ] Store device tokens.
- [ ] Create preferred stop subscription.
- [ ] Notify when shuttle starts.
- [ ] Notify when shuttle is close to preferred stop.
- [ ] Notify when shuttle is delayed.
- [ ] Notify when shuttle is cancelled.
- [ ] Notify when shuttle goes offline.
- [ ] Prevent duplicate notifications.
- [ ] Allow users to disable notifications.

## Notification Examples

```txt
Campus Shuttle is active.
Campus Shuttle is about 5 minutes from Off-Campus Housing.
Campus Shuttle has been delayed.
Campus Shuttle has been cancelled.
Campus Shuttle location is currently unavailable.
```

## Completion Criteria

- [ ] Students can receive push notifications.
- [ ] Notifications are based on trip state and preferred stop.

---

# Phase 13 — Offline and Stale GPS Detection

## Goals

Detect when shuttle tracking is no longer reliable.

## Checklist

- [ ] Track last GPS ping timestamp.
- [ ] Mark location stale after 60 seconds.
- [ ] Mark shuttle offline after 3–5 minutes.
- [ ] Return stale status to student app.
- [ ] Show offline warning in student app.
- [ ] Notify admins if shuttle goes offline.
- [ ] Allow driver to resume tracking.

## Suggested Rules

```txt
No ping for 60 seconds:
    is_location_stale = true

No ping for 3–5 minutes:
    trip status = offline
```

## Completion Criteria

- [ ] Student app does not show stale GPS as fresh.
- [ ] Admin can see offline/stale shuttle state.

---

# Phase 14 — Admin Dashboard

## Goals

Build dashboard for operations management.

## Checklist

- [ ] Create Next.js dashboard.
- [ ] Add admin login.
- [ ] Add dashboard overview.
- [ ] Add stops management.
- [ ] Add routes management.
- [ ] Add route stop ordering.
- [ ] Add shuttle management.
- [ ] Add driver management.
- [ ] Add timetable management.
- [ ] Add active trips page.
- [ ] Add trip history page.
- [ ] Add announcements page.
- [ ] Add delay/cancellation management.

## Completion Criteria

- [ ] Admin can manage the full shuttle system.
- [ ] Admin can view live and historical trip information.

---

# Phase 15 — Testing

## Goals

Test backend, mobile apps, and live tracking flow.

## Backend Tests

- [ ] Test authentication.
- [ ] Test route creation.
- [ ] Test stop creation.
- [ ] Test trip start.
- [ ] Test GPS ping ingestion.
- [ ] Test Redis live state update.
- [ ] Test location history storage.
- [ ] Test ETA calculation.
- [ ] Test next stop override.
- [ ] Test trip ending.
- [ ] Test stale GPS detection.

## Mobile Tests

- [ ] Test driver login.
- [ ] Test GPS permission.
- [ ] Test background GPS updates.
- [ ] Test start trip.
- [ ] Test change next stop.
- [ ] Test end trip.
- [ ] Test student map display.
- [ ] Test ETA display.
- [ ] Test no-active-shuttle state.

## Real-World Tests

- [ ] Test with simulated GPS.
- [ ] Test with a real phone moving around campus.
- [ ] Test route A → B → C → A.
- [ ] Test route A → B → A.
- [ ] Test driver changing next stop.
- [ ] Test no network condition.
- [ ] Test stale GPS warning.
- [ ] Test notifications.

## Completion Criteria

- [ ] End-to-end tracking works reliably.
- [ ] The shuttle marker updates correctly.
- [ ] ETA is reasonable.
- [ ] Driver controls work.
- [ ] Student app handles errors clearly.

---

# Phase 16 — Deployment

## Goals

Deploy the MVP system.

## Checklist

- [ ] Configure production environment variables.
- [ ] Deploy PostgreSQL.
- [ ] Deploy Redis.
- [ ] Deploy FastAPI backend.
- [ ] Deploy admin dashboard.
- [ ] Configure Firebase Cloud Messaging.
- [ ] Configure map provider keys.
- [ ] Set up logging.
- [ ] Set up monitoring.
- [ ] Set up database backups.
- [ ] Set up HTTPS.
- [ ] Test production APIs.
- [ ] Test mobile apps against production backend.

## Completion Criteria

- [ ] Production backend is live.
- [ ] Student app connects to production backend.
- [ ] Driver app sends GPS to production backend.
- [ ] Admin dashboard works in production.

---

# Phase 17 — Future Improvements

## Checklist

- [ ] Add geofencing around stops.
- [ ] Add automatic stop arrival detection.
- [ ] Add road-based ETA with OSRM, Mapbox, or Google Routes.
- [ ] Add route polylines.
- [ ] Add dedicated Android shuttle phone support.
- [ ] Add trip analytics.
- [ ] Add shuttle performance reports.
- [ ] Add driver shift scheduling.
- [ ] Add maintenance tracking.
- [ ] Add occupancy reporting.
- [ ] Add student feedback dashboard.
- [ ] Add admin audit logs.
- [ ] Add multi-campus support.

---

# Final Build Rule

Build the system in this order:

```txt
Backend first
↓
Driver GPS flow
↓
Student live map
↓
ETA and next stop
↓
Notifications
↓
Admin dashboard
↓
Production improvements
```

Do not start with advanced routing. First prove the core live-tracking experience.
