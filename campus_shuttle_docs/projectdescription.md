# Campus Shuttle Tracking System — Project Description

## 1. Project Summary

The Campus Shuttle Tracking System is a real-time transportation visibility platform designed for students who depend on school shuttles, especially students living off-campus. The system allows students to see whether a shuttle is active, where it is currently located, what stop it is heading to next, and when it is expected to arrive.

The main purpose of the system is to reduce uncertainty. Instead of students waiting outside without knowing whether the shuttle is coming, delayed, cancelled, offline, or already passed, the app provides live shuttle status and location information.

The system uses a hybrid shuttle-routing model:

- Predefined routes give the shuttle system structure.
- Driver-selected next stops give the system flexibility.
- The driver or shuttle phone provides live GPS tracking.
- The timetable acts as the expected schedule.
- Live GPS is treated as the actual source of truth.

This design keeps the system simple, realistic, and scalable for a campus environment.

---

## 2. Problem Statement

Many students rely on campus shuttles to move between off-campus housing, sub-campuses, and the main campus. However, traditional shuttle systems often depend only on fixed timetables. This creates several problems:

- Students do not know whether the shuttle is currently active.
- Students do not know where the shuttle is located.
- Students cannot tell whether the shuttle is delayed.
- Students may wait after the shuttle has already passed.
- Students may miss class, work, or events because the shuttle schedule is unreliable.
- Administrators have limited visibility into trip history and shuttle performance.

A timetable alone is not enough because real trips are affected by traffic, delays, driver decisions, weather, route changes, and operational issues.

---

## 3. Main Goal

The goal is to build a real-time shuttle tracking system that answers the most important student questions:

- Is the shuttle active?
- Where is the shuttle right now?
- What is the next stop?
- What is the estimated arrival time?
- Is the shuttle delayed, cancelled, offline, paused, or completed?
- Can I receive a notification when the shuttle is close to my preferred stop?

---

## 4. Core Users

### Students

Students use the app to view live shuttle information.

Student users should be able to:

- View active shuttles without logging in.
- See shuttle location on a map.
- See shuttle status.
- See the next stop.
- See estimated arrival time.
- View the timetable.
- Receive notifications after logging in.
- Select a preferred stop after logging in.
- Submit feedback or report issues after logging in.

### Drivers

Drivers use a simple driver app to start and manage shuttle trips.

Driver users should be able to:

- Log in.
- Select an assigned shuttle or route.
- Start a trip.
- Send live GPS location automatically.
- Change the next stop when needed.
- Report a delay.
- Cancel a trip if necessary.
- End a trip.

The driver should not manually update every movement. GPS should handle most of the tracking.

### Administrators

Administrators use a dashboard to manage the shuttle system.

Admin users should be able to:

- Manage stops.
- Manage routes.
- Manage route stop order.
- Manage shuttles.
- Manage drivers.
- Manage timetables.
- View trip history.
- View active trips.
- Send announcements.
- Create delay or cancellation messages.
- Monitor stale/offline shuttle status.

---

## 5. System Approach

The system follows a hybrid routing model.

Instead of storing every possible route combination, the system stores:

- Stops
- Routes
- Ordered route stops
- Trips
- Current next stop
- Live shuttle location

The system does not need to know every possible path permutation. It only needs to know:

```txt
Current shuttle location → Selected next stop
```

This keeps the logic simple and flexible.

For example, stops may include:

```txt
A = Main Campus
B = Off-Campus Housing
C = Sub-Campus / Another Location
```

Routes may include:

```txt
A → B → C → A
A → B → A
A → C → A
```

However, if the driver needs to change direction, the driver can update the next stop manually. The student app updates immediately.

---

## 6. Tracking Strategy

For the MVP, the system will not use expensive dedicated GPS hardware.

Instead:

1. The driver opens the driver app.
2. The driver selects a route.
3. The driver taps “Start Trip.”
4. The driver phone sends GPS coordinates to the backend.
5. The backend stores the latest live location in Redis.
6. The backend stores historical pings in PostgreSQL.
7. Students see the shuttle move on the map.

A dedicated Android phone may later be placed permanently inside each shuttle to improve reliability and avoid depending on a driver’s personal phone.

---

## 7. ETA Strategy

ETA is calculated using:

- Current shuttle GPS location
- Next stop location
- Estimated or calculated average speed

Basic MVP formula:

```txt
ETA = distance_to_next_stop / average_speed
```

For the MVP:

- Use a default average speed, such as 15–25 mph.
- Calculate distance between the current shuttle location and next stop.
- Convert the result into estimated minutes.

Later versions can improve ETA by:

- Calculating speed from recent GPS pings.
- Averaging the last 5–10 speed values.
- Using road distance instead of straight-line distance.
- Integrating OSRM, Mapbox Directions, or Google Routes.
- Factoring in traffic and historical shuttle performance.

---

## 8. Timetable Role

The timetable is not the main source of truth. It is the expected plan.

```txt
Timetable = expected schedule
Live GPS = actual truth
```

Each trip should store:

- Scheduled start time
- Actual start time
- Actual end time
- Current status
- Current stop
- Next stop

Example statuses:

- Scheduled
- Active
- Delayed
- Paused
- Completed
- Cancelled
- Offline

---

## 9. Key Features

### MVP Features

- Driver login
- Start trip
- End trip
- Send GPS location
- Change next stop
- Report delay
- Cancel trip
- View live shuttle location
- View active shuttle status
- View next stop
- View ETA
- View timetable
- Basic admin management

### Future Features

- Push notifications
- Preferred stop subscriptions
- Geofencing near stops
- Automatic stop arrival detection
- Road-based ETA
- Dedicated shuttle phone support
- Driver assignment scheduling
- Historical analytics
- Occupancy tracking
- Multi-shuttle support
- Maintenance tracking

---

## 10. Final Product Vision

The final system should make shuttle transportation more predictable and transparent for students. Students should no longer have to guess whether the shuttle is coming. Drivers should have a simple tool that does not distract them. Administrators should have enough control to manage routes, stops, drivers, shuttles, timetables, and trip history.

The system should remain simple, flexible, and realistic.

Final architecture:

```txt
Driver Phone → Backend API → Redis/PostgreSQL → Student App/Admin Dashboard
```
