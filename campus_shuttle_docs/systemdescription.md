# Campus Shuttle Tracking System — System Description

## System Name

Campus Shuttle Tracking System

---

## System Purpose

The Campus Shuttle Tracking System is designed to provide real-time visibility into campus shuttle movement. The system helps students know whether a shuttle is active, where it is located, what stop it is heading to next, and when it is expected to arrive.

The system is especially useful for off-campus students who rely on the shuttle to travel between housing, school buildings, sub-campuses, and the main campus.

---

## System Description

The system uses the driver’s phone or a dedicated shuttle phone as the GPS source. When the driver starts a trip, the phone sends GPS coordinates to the backend. The backend stores the latest shuttle location in Redis for fast live access and stores historical location pings in PostgreSQL for records and analysis.

Students use the mobile app to view the shuttle on a map. The student app displays the shuttle’s current status, next stop, estimated arrival time, and timetable information.

Administrators use a dashboard to manage routes, stops, drivers, shuttles, timetables, announcements, and trip history.

---

## System Navigation Logic

The system uses predefined routes for structure but does not depend on rigid route combinations.

Instead of storing every possible route path, the system calculates:

```txt
Current shuttle location → Next stop
```

The driver can change the next stop at any time. This allows flexibility if the shuttle changes direction, skips a stop, or follows a different pattern.

---

## Main System Modules

## 1. Student Module

Allows students to:

- View live shuttle location
- View ETA
- View next stop
- View shuttle status
- View timetable
- Receive notifications
- Select preferred stop

## 2. Driver Module

Allows drivers to:

- Log in
- Start trip
- Send GPS location
- Change next stop
- Report delay
- Cancel trip
- End trip

## 3. Admin Module

Allows admins to:

- Manage routes
- Manage stops
- Manage shuttles
- Manage drivers
- Manage timetables
- View trip history
- Send announcements

## 4. Backend Module

Handles:

- Authentication
- Trip management
- GPS ingestion
- ETA calculation
- Redis live state
- Database storage
- Notification triggers

## 5. Notification Module

Handles:

- Shuttle start alerts
- Delay alerts
- Cancellation alerts
- Shuttle approaching alerts
- Offline tracking alerts

---

## System Statuses

Trip statuses:

- Scheduled
- Active
- Delayed
- Paused
- Completed
- Cancelled
- Offline

Shuttle statuses:

- Inactive
- Active
- Maintenance
- Offline

---

## Final System Principle

The system should be simple, flexible, and realistic.

```txt
Timetable = expected plan
Live GPS = actual truth
Next stop = current navigation target
```
