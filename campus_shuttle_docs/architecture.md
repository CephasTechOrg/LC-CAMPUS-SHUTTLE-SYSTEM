# Campus Shuttle Tracking System — Architecture

## 1. Architecture Goal

The architecture is designed to support real-time shuttle tracking, simple driver control, fast student access, reliable historical storage, and future scalability.

The system should be easy to build as an MVP but strong enough to grow into a production shuttle platform.

---

## 2. High-Level Architecture

```txt
Driver App
   ↓
FastAPI Backend
   ↓
Redis + PostgreSQL/PostGIS
   ↓
Student App + Admin Dashboard
```

Detailed flow:

```txt
Driver Phone GPS
   ↓
Driver Mobile App
   ↓
FastAPI API
   ↓
Redis stores latest shuttle location
PostgreSQL stores trips, users, stops, routes, and location history
   ↓
Student App reads live shuttle state
Admin Dashboard manages system data
```

---

## 3. Main Components

## 3.1 Driver Mobile App

The driver app is responsible for starting and managing trips.

Driver app responsibilities:

- Driver login
- Select route
- Select shuttle
- Start trip
- Send GPS pings
- Change next stop
- Report delay
- Cancel trip
- End trip

The app should send GPS updates every few seconds while a trip is active.

Example location ping:

```json
{
  "trip_id": 12,
  "latitude": 35.12345,
  "longitude": -80.12345,
  "speed": 18.4,
  "heading": 90
}
```

---

## 3.2 Student Mobile App

The student app is responsible for displaying shuttle information.

Student app responsibilities:

- View active shuttle
- View shuttle marker on map
- View next stop
- View ETA
- View shuttle status
- View timetable
- Receive notifications
- Select preferred stop after login

Students should be able to view the live shuttle map without logging in.

---

## 3.3 Admin Dashboard

The admin dashboard is used to manage shuttle operations.

Admin dashboard responsibilities:

- Manage stops
- Manage routes
- Manage route stop order
- Manage shuttles
- Manage drivers
- Manage timetable
- View trip history
- View active trips
- Send announcements
- Manage delay/cancellation messages

Recommended technology:

```txt
Next.js + TypeScript
```

---

## 3.4 Backend API

The backend is the brain of the system.

Backend responsibilities:

- Authentication and authorization
- Trip management
- GPS ingestion
- ETA calculation
- Next stop management
- Live shuttle state management
- Timetable management
- Notification triggers
- Admin management APIs

Recommended technology:

```txt
FastAPI
```

---

## 3.5 PostgreSQL + PostGIS

PostgreSQL stores permanent system data.

Stored data includes:

- Users
- Drivers
- Shuttles
- Stops
- Routes
- Route stops
- Trips
- Location history
- Subscriptions
- Timetable entries
- Announcements

PostGIS should be used for location-aware queries such as:

- Distance between shuttle and stop
- Stops near shuttle
- Geofence detection
- Nearby shuttle queries

---

## 3.6 Redis

Redis stores fast-changing live data.

Redis should store:

- Latest shuttle location
- Active trip state
- Last GPS ping timestamp
- Current ETA
- Current speed estimate
- Current next stop
- Stale/offline flags

Example Redis keys:

```txt
trip:12:live_location
trip:12:last_ping
trip:12:eta
trip:12:status
trip:12:next_stop
```

Redis should not be the permanent source of trip history. PostgreSQL should remain the permanent source.

---

## 3.7 Firebase Cloud Messaging

Firebase Cloud Messaging is used for push notifications.

Notification examples:

- Shuttle started
- Shuttle is 5 minutes away
- Shuttle delayed
- Shuttle cancelled
- Shuttle offline
- Shuttle reached preferred stop

---

## 3.8 Map Provider

The map provider is mainly used for visual display in the MVP.

Possible providers:

- Google Maps
- Mapbox
- OpenStreetMap-based maps

For MVP, the map should display:

- Shuttle marker
- Stop markers
- Optional route line
- Student’s selected/preferred stop

The map provider should not be the brain of the system. The backend owns the trip state and live location.

---

## 4. Data Flow

## 4.1 Starting a Trip

```txt
Driver selects route
↓
Driver selects shuttle
↓
Driver taps Start Trip
↓
Backend creates trip record
↓
Trip status becomes Active
↓
Backend stores active trip in PostgreSQL and Redis
```

---

## 4.2 Sending GPS Location

```txt
Driver phone gets GPS coordinates
↓
Driver app sends location ping to backend
↓
Backend validates active trip
↓
Backend stores latest location in Redis
↓
Backend stores historical ping in PostgreSQL
↓
Backend recalculates ETA
↓
Student app receives updated shuttle state
```

---

## 4.3 Student Viewing Live Shuttle

```txt
Student opens app
↓
App requests active shuttle/trip
↓
Backend reads latest live state from Redis
↓
Backend returns shuttle location, status, next stop, and ETA
↓
Student sees shuttle on map
```

---

## 4.4 Driver Changing Next Stop

```txt
Driver taps Change Next Stop
↓
Driver selects stop
↓
Backend updates trip.next_stop_id
↓
Redis live trip state is updated
↓
ETA is recalculated
↓
Student app updates immediately
```

---

## 4.5 Detecting Offline/Stale Shuttle

A shuttle should be considered stale if no GPS ping is received for a defined period.

Example rule:

```txt
If last GPS ping is older than 60 seconds:
    mark location as stale

If last GPS ping is older than 3–5 minutes:
    mark shuttle as offline
```

The backend should expose this status to students and admins.

---

## 5. API Architecture

## 5.1 Driver APIs

```txt
POST   /api/v1/driver/trips/start
POST   /api/v1/driver/trips/{trip_id}/location
PATCH  /api/v1/driver/trips/{trip_id}/next-stop
PATCH  /api/v1/driver/trips/{trip_id}/delay
PATCH  /api/v1/driver/trips/{trip_id}/cancel
POST   /api/v1/driver/trips/{trip_id}/end
```

---

## 5.2 Student APIs

```txt
GET    /api/v1/student/shuttles/active
GET    /api/v1/student/trips/{trip_id}/live
GET    /api/v1/student/routes
GET    /api/v1/student/timetable
POST   /api/v1/student/subscriptions
DELETE /api/v1/student/subscriptions/{subscription_id}
```

---

## 5.3 Admin APIs

```txt
POST   /api/v1/admin/stops
GET    /api/v1/admin/stops
PATCH  /api/v1/admin/stops/{stop_id}
DELETE /api/v1/admin/stops/{stop_id}

POST   /api/v1/admin/routes
GET    /api/v1/admin/routes
PATCH  /api/v1/admin/routes/{route_id}
DELETE /api/v1/admin/routes/{route_id}

POST   /api/v1/admin/routes/{route_id}/stops
PATCH  /api/v1/admin/routes/{route_id}/stops/reorder

POST   /api/v1/admin/shuttles
GET    /api/v1/admin/shuttles
PATCH  /api/v1/admin/shuttles/{shuttle_id}

POST   /api/v1/admin/drivers
GET    /api/v1/admin/drivers
PATCH  /api/v1/admin/drivers/{driver_id}

POST   /api/v1/admin/timetable
GET    /api/v1/admin/timetable

GET    /api/v1/admin/trips
GET    /api/v1/admin/trips/{trip_id}
```

---

## 6. Realtime Strategy

There are three possible approaches:

### Option 1 — Polling

The student app requests live data every few seconds.

Pros:

- Simple to build
- Reliable for MVP
- Easy to debug

Cons:

- More repeated requests
- Less efficient than realtime sockets

Recommended MVP interval:

```txt
Every 5–10 seconds
```

### Option 2 — Server-Sent Events

Backend pushes one-way updates to student app.

Pros:

- Better than polling
- Good for one-way live updates

Cons:

- Less flexible than WebSockets

### Option 3 — WebSockets

Backend and client maintain live connection.

Pros:

- Best realtime experience
- Smooth live shuttle updates

Cons:

- More complex
- Requires connection management

Recommended approach:

```txt
MVP: Polling
Improved version: Server-Sent Events or WebSockets
Production: WebSockets
```

---

## 7. ETA Architecture

## 7.1 MVP ETA

```txt
ETA = distance_to_next_stop / average_speed
```

Use:

- Current latitude/longitude
- Next stop latitude/longitude
- Default speed, such as 15–25 mph

## 7.2 Improved ETA

Use GPS speed calculated from recent location pings.

```txt
Speed = distance between GPS points / time difference
```

Average the last 5–10 speed values to avoid unstable readings.

## 7.3 Production ETA

Use road-based routing:

- OSRM
- Mapbox Directions
- Google Routes

---

## 8. Authentication and Authorization

Suggested roles:

```txt
student
driver
admin
```

Access rules:

- Public users can view active shuttle data.
- Students must log in for notifications, preferred stop, and feedback.
- Drivers must log in to start/end trips and send location.
- Admins must log in to manage system data.

---

## 9. Deployment Architecture

Recommended deployment:

```txt
Mobile Apps:
- App Store / Play Store / internal school distribution

Backend:
- Dockerized FastAPI service

Database:
- PostgreSQL with PostGIS

Cache:
- Redis

Admin Dashboard:
- Next.js deployed separately

Notifications:
- Firebase Cloud Messaging
```

Possible hosting options:

- Render
- Fly.io
- Railway
- AWS
- Google Cloud
- Azure

---

## 10. Final Architecture Principle

The backend should own the real shuttle state.

```txt
Driver phone provides GPS.
Backend validates and processes GPS.
Redis stores latest live state.
PostgreSQL stores permanent history.
Student app displays the result.
Admin dashboard manages the system.
```
