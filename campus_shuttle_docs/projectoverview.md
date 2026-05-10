# Campus Shuttle Tracking System — Project Overview

## Overview

The Campus Shuttle Tracking System is a real-time shuttle visibility platform for students, drivers, and school administrators. It helps students track the school shuttle live, view its status, see the next stop, and estimate when it will arrive.

The system is designed for students who live off-campus and depend on the school shuttle to reach campus on time.

---

## Why This System Is Needed

A fixed timetable alone does not solve the shuttle problem. A shuttle can be delayed, cancelled, offline, ahead of schedule, or rerouted. Students need real-time information, not only scheduled information.

This system solves that problem by combining:

- Predefined routes
- Driver-controlled next stop updates
- Live GPS from the driver or shuttle phone
- Fast backend location updates
- Student-facing map and ETA display
- Admin tools for managing the shuttle operation

---

## Core Idea

The system should always answer:

```txt
Where is the shuttle now?
Where is it going next?
How long until it gets there?
What is its current status?
```

The system should not store every possible route combination. Instead, it should calculate the shuttle’s movement based on:

```txt
Current shuttle GPS location → Next stop
```

This makes the system simple, flexible, and realistic.

---

## User Roles

### Student

Students can:

- View active shuttle location.
- View shuttle status.
- View next stop.
- View ETA.
- View timetable.
- Receive notifications after logging in.
- Select a preferred stop after logging in.

Students should not need an account just to view the live shuttle map.

### Driver

Drivers can:

- Log in.
- Select a route.
- Start a trip.
- Send GPS location automatically.
- Change the next stop.
- Report delay.
- Cancel trip.
- End trip.

### Admin

Admins can:

- Manage routes.
- Manage stops.
- Manage timetables.
- Manage drivers.
- Manage shuttles.
- Send announcements.
- View active and past trips.

---

## Recommended Stack

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

## MVP Scope

The MVP should prove the core tracking flow:

```txt
Driver starts trip
↓
Driver phone sends GPS
↓
Backend stores live location
↓
Student app displays shuttle on map
↓
ETA updates based on current location and next stop
```

The MVP does not need complex routing, traffic prediction, or expensive GPS hardware.

---

## MVP Phases

### Phase 1 — Backend Foundation

- Create database models.
- Create authentication.
- Create route, stop, shuttle, driver, and trip APIs.

### Phase 2 — Driver App

- Driver can log in.
- Driver can start trip.
- Driver phone sends GPS.
- Driver can change next stop.
- Driver can end trip.

### Phase 3 — Student App

- Student can view active shuttle.
- Student can see map.
- Student can see ETA.
- Student can see next stop.

### Phase 4 — Notifications

- Notify when shuttle starts.
- Notify when shuttle is close.
- Notify delay or cancellation.

### Phase 5 — Admin Dashboard

- Manage routes, stops, timetable, drivers, shuttles, and announcements.

### Phase 6 — Testing

- Test GPS updates.
- Test ETA.
- Test route changes.
- Test stale GPS/offline detection.

---

## Success Criteria

The MVP is successful when:

- A driver can start a trip.
- GPS pings are sent to the backend.
- The latest location is stored in Redis.
- Trip history is stored in PostgreSQL.
- Students can see the active shuttle on a map.
- Students can see the next stop and ETA.
- The driver can change the next stop.
- The system detects stale/offline location updates.

---

## Final Principle

Keep the system simple first.

```txt
Timetable = planned schedule
Live GPS = actual truth
Next stop = current navigation target
ETA = current location to next stop
```
