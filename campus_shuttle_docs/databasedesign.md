# Campus Shuttle Tracking System — Database Design

## 1. Database Goal

The database should store permanent system data, including users, drivers, shuttles, stops, routes, trips, schedules, and location history.

The database should not be used as the only live-location engine. Fast-changing live shuttle state should be cached in Redis, while PostgreSQL stores reliable permanent history.

Recommended database:

```txt
PostgreSQL + PostGIS
```

PostGIS is recommended because this project depends heavily on geographic coordinates, distance calculation, and future geofencing.

---

## 2. Core Tables

The first version should include these main tables:

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

## 3. Entity Relationship Summary

```txt
users
  └── drivers

drivers
  └── trips

shuttles
  └── trips
  └── location_pings

routes
  └── route_stops
  └── trips
  └── timetable_entries

stops
  └── route_stops
  └── trips.current_stop_id
  └── trips.next_stop_id
  └── subscriptions

trips
  └── location_pings
```

---

## 4. Table Designs

## 4.1 users

Stores all users in the system.

Roles:

- student
- driver
- admin

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT,
    role VARCHAR(30) NOT NULL CHECK (role IN ('student', 'driver', 'admin')),
    preferred_stop_id UUID REFERENCES stops(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Notes:

- Students may not need an account to view live shuttle data.
- Accounts are required for notifications, preferred stops, feedback, drivers, and admins.

---

## 4.2 stops

Stores shuttle stops.

```sql
CREATE TABLE stops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    description TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    location GEOGRAPHY(Point, 4326),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Recommended index:

```sql
CREATE INDEX idx_stops_location ON stops USING GIST (location);
```

---

## 4.3 routes

Stores route definitions.

```sql
CREATE TABLE routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Example route names:

- Main Campus → Off-Campus Housing → Main Campus
- Main Campus → Sub-Campus → Main Campus
- Full Loop Route

---

## 4.4 route_stops

Stores ordered stops for each route.

```sql
CREATE TABLE route_stops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id UUID NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    stop_id UUID NOT NULL REFERENCES stops(id),
    stop_order INTEGER NOT NULL,
    estimated_minutes_from_previous INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(route_id, stop_order),
    UNIQUE(route_id, stop_id)
);
```

Notes:

- This gives the route structure.
- The system should still allow the driver to override the next stop.

---

## 4.5 shuttles

Stores shuttle vehicles.

```sql
CREATE TABLE shuttles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    plate_number VARCHAR(50),
    status VARCHAR(30) NOT NULL DEFAULT 'inactive'
        CHECK (status IN ('inactive', 'active', 'maintenance', 'offline')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 4.6 drivers

Stores driver profiles linked to users.

```sql
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_shuttle_id UUID REFERENCES shuttles(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 4.7 trips

Stores each shuttle trip.

```sql
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id UUID NOT NULL REFERENCES routes(id),
    shuttle_id UUID NOT NULL REFERENCES shuttles(id),
    driver_id UUID NOT NULL REFERENCES drivers(id),

    scheduled_start_time TIMESTAMPTZ,
    actual_start_time TIMESTAMPTZ,
    actual_end_time TIMESTAMPTZ,

    current_stop_id UUID REFERENCES stops(id),
    next_stop_id UUID REFERENCES stops(id),

    status VARCHAR(30) NOT NULL DEFAULT 'scheduled'
        CHECK (status IN (
            'scheduled',
            'active',
            'delayed',
            'paused',
            'completed',
            'cancelled',
            'offline'
        )),

    delay_reason TEXT,
    cancellation_reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Recommended indexes:

```sql
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trips_route_id ON trips(route_id);
CREATE INDEX idx_trips_shuttle_id ON trips(shuttle_id);
CREATE INDEX idx_trips_driver_id ON trips(driver_id);
CREATE INDEX idx_trips_actual_start_time ON trips(actual_start_time);
```

---

## 4.8 location_pings

Stores historical GPS pings.

```sql
CREATE TABLE location_pings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    shuttle_id UUID NOT NULL REFERENCES shuttles(id),

    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    location GEOGRAPHY(Point, 4326),

    speed_mph DOUBLE PRECISION,
    heading DOUBLE PRECISION,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Recommended indexes:

```sql
CREATE INDEX idx_location_pings_trip_id ON location_pings(trip_id);
CREATE INDEX idx_location_pings_shuttle_id ON location_pings(shuttle_id);
CREATE INDEX idx_location_pings_created_at ON location_pings(created_at);
CREATE INDEX idx_location_pings_location ON location_pings USING GIST (location);
```

Notes:

- This table can grow quickly.
- For production, consider partitioning by date or trip.
- Redis should store the latest live location to avoid reading from this table on every student request.

---

## 4.9 subscriptions

Stores student notification preferences.

```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stop_id UUID NOT NULL REFERENCES stops(id),
    notify_minutes_before INTEGER NOT NULL DEFAULT 5,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(user_id, stop_id)
);
```

---

## 4.10 timetable_entries

Stores planned shuttle schedule.

```sql
CREATE TABLE timetable_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id UUID NOT NULL REFERENCES routes(id),
    shuttle_id UUID REFERENCES shuttles(id),

    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    scheduled_start_time TIME NOT NULL,
    scheduled_end_time TIME,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Day of week convention:

```txt
0 = Sunday
1 = Monday
2 = Tuesday
3 = Wednesday
4 = Thursday
5 = Friday
6 = Saturday
```

---

## 4.11 announcements

Stores admin announcements.

```sql
CREATE TABLE announcements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    audience VARCHAR(30) NOT NULL DEFAULT 'all'
        CHECK (audience IN ('all', 'students', 'drivers')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ
);
```

---

## 5. Redis Live Data Design

Redis should store the latest live shuttle state.

Example key:

```txt
trip:{trip_id}:live
```

Example value:

```json
{
  "trip_id": "uuid",
  "shuttle_id": "uuid",
  "route_id": "uuid",
  "status": "active",
  "latitude": 35.12345,
  "longitude": -80.12345,
  "speed_mph": 18.5,
  "heading": 90,
  "next_stop_id": "uuid",
  "next_stop_name": "Off-Campus Housing",
  "eta_minutes": 7,
  "last_ping_at": "2026-05-09T14:32:00Z",
  "is_location_stale": false
}
```

Recommended Redis keys:

```txt
active_trips
trip:{trip_id}:live
shuttle:{shuttle_id}:active_trip
trip:{trip_id}:speed_samples
```

---

## 6. Important Design Rules

## Rule 1 — PostgreSQL stores permanent truth

Use PostgreSQL for:

- Users
- Drivers
- Stops
- Routes
- Trips
- Timetables
- Location history
- Subscriptions
- Announcements

## Rule 2 — Redis stores live truth

Use Redis for:

- Latest shuttle location
- Current ETA
- Last GPS ping timestamp
- Active trip state
- Speed samples

## Rule 3 — Do not store every route combination

Store route structure, but calculate:

```txt
Current shuttle location → Next stop
```

## Rule 4 — Driver next-stop override is required

The trip table must support:

```txt
next_stop_id
```

This lets the driver update the next destination at any time.

---

## 7. Future Database Improvements

Future improvements may include:

- device_tokens table for push notifications
- feedback_reports table
- trip_events table
- shuttle_maintenance table
- driver_shift table
- route_polylines table
- stop_geofences table
- occupancy_reports table
- location_pings partitioning
- audit_logs table

---

## 8. Suggested Additional Tables for Production

## 8.1 device_tokens

```sql
CREATE TABLE device_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    platform VARCHAR(30) CHECK (platform IN ('ios', 'android', 'web')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_used_at TIMESTAMPTZ
);
```

## 8.2 trip_events

```sql
CREATE TABLE trip_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Possible event types:

- trip_started
- trip_ended
- next_stop_changed
- delay_reported
- trip_cancelled
- shuttle_offline
- shuttle_online
- stop_arrived

---

## 9. Final Database Principle

The database design should support the MVP without overcomplicating it.

The most important entities are:

```txt
stops
routes
route_stops
shuttles
drivers
trips
location_pings
subscriptions
```

The most important live-state rule is:

```txt
Use Redis for the latest shuttle state.
Use PostgreSQL for permanent history.
```
