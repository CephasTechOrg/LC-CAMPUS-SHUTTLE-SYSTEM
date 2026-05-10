# Campus Shuttle Tracking System

A real-time campus shuttle tracking system for students who depend on school shuttles, especially students living off-campus.

The system allows students to view live shuttle location, shuttle status, next stop, ETA, timetable, delay updates, cancellation notices, and notifications.

---

## Project Purpose

Students often wait for the shuttle without knowing whether it is coming, delayed, cancelled, offline, or already passed. A timetable alone is not reliable enough because real shuttle movement can change.

This project solves that problem by using live GPS tracking from the driver or shuttle phone.

---

## Core System Idea

The system uses a hybrid routing model:

```txt
Predefined routes = structure
Driver next-stop override = flexibility
Driver/shuttle phone GPS = live truth
Timetable = expected plan
Backend = system brain
Map provider = visual display
```

The system should not store every possible route combination.

Instead, it should always calculate:

```txt
Current shuttle location → Next stop → ETA
```

---

## Main Features

## Student App

Students can:

- View active shuttle location.
- View shuttle status.
- View next stop.
- View ETA.
- View timetable.
- Receive notifications.
- Select preferred stop.
- Report feedback.

Students should not need to log in just to view the live shuttle map.

## Driver App

Drivers can:

- Log in.
- Select route.
- Start trip.
- Send GPS location automatically.
- Change next stop.
- Report delay.
- Cancel trip.
- End trip.

## Admin Dashboard

Admins can:

- Manage stops.
- Manage routes.
- Manage route stop order.
- Manage shuttles.
- Manage drivers.
- Manage timetables.
- Send announcements.
- View active trips.
- View trip history.

---

## Recommended Tech Stack

```txt
Mobile App: Flutter
Admin Dashboard: Next.js + TypeScript
Backend: FastAPI
Database: PostgreSQL + PostGIS
Live Location Cache: Redis
Notifications: Firebase Cloud Messaging
Maps: Mapbox or Google Maps
Routing/ETA: MVP formula first, OSRM/Mapbox/Google later
Deployment: Docker-based deployment
```

---

## High-Level Architecture

```txt
Driver Phone
   ↓
Driver App sends GPS
   ↓
FastAPI Backend
   ↓
Redis stores latest live location
PostgreSQL stores permanent data/history
   ↓
Student App and Admin Dashboard display shuttle state
```

---

## MVP Goal

The first version should prove this flow:

```txt
Driver starts trip
↓
Phone sends GPS
↓
Backend stores live location
↓
Student sees shuttle on map
↓
ETA updates based on current location and next stop
```

---

## Core Data Models

- users
- drivers
- shuttles
- stops
- routes
- route_stops
- trips
- location_pings
- subscriptions
- timetable_entries
- announcements

---

## Suggested Repository Structure

```txt
campus-shuttle-tracker/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── mobile/
│   ├── student_app/
│   └── driver_app/
│
├── admin-dashboard/
│
├── docs/
│   ├── projectdescription.md
│   ├── projectoverview.md
│   ├── architecture.md
│   ├── databasedesign.md
│   └── todo.md
│
└── README.md
```

---

## Main Backend API Groups

```txt
/api/v1/auth
/api/v1/driver
/api/v1/student
/api/v1/admin
/api/v1/trips
/api/v1/routes
/api/v1/stops
/api/v1/shuttles
/api/v1/timetable
```

---

## Development Phases

1. Backend foundation
2. Database models
3. Driver trip flow
4. GPS ingestion
5. Redis live location
6. Student live map
7. ETA calculation
8. Next-stop override
9. Notifications
10. Admin dashboard
11. Testing and deployment

---

## Important Design Decisions

### Live GPS is the source of truth

The timetable is useful, but the actual shuttle location should come from live GPS.

### Redis is used for live state

The student app should not query historical GPS records every few seconds. Redis should hold the latest shuttle location.

### PostgreSQL stores history

PostgreSQL should store trips, users, stops, routes, and historical GPS pings.

### Driver app must stay simple

Drivers should only need to start a trip, change the next stop if necessary, report delays, cancel, and end the trip.

### Students should not need login for public tracking

Public live shuttle tracking should be available without authentication.

---

## Future Improvements

- Geofencing near stops
- Automatic stop arrival detection
- Road-based ETA
- Dedicated shuttle phone in each vehicle
- WebSocket live updates
- Historical analytics
- Multi-shuttle support
- Maintenance management
- Driver shift scheduling
- Occupancy reporting
- Admin audit logs

---

## Final Principle

Keep the system simple, flexible, and realistic.

```txt
Driver Phone → Backend API → Redis/PostgreSQL → Student App/Admin Dashboard
```
