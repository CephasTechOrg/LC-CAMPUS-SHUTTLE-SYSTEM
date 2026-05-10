# Campus Shuttle Tracking System — Folder Structure

## 1. Purpose

This document defines the recommended folder structure for the Campus Shuttle Tracking System.

The project uses:

```txt
Backend: FastAPI
Mobile App: Flutter
Database: PostgreSQL + PostGIS
Live Cache: Redis
Notifications: Firebase Cloud Messaging
Maps: Mapbox or Google Maps
```

For now, the project focuses more on the core shuttle-tracking system than the admin dashboard. The main priority is:

```txt
Driver starts trip
↓
Driver phone sends GPS
↓
Backend receives and processes location
↓
Redis stores latest live shuttle state
↓
PostgreSQL stores permanent trip/location history
↓
Student app displays shuttle location, ETA, and next stop
```

---

## 2. Recommended Top-Level Structure

```txt
campus-shuttle-tracker/
│
├── backend/
│   └── FastAPI backend system
│
├── mobile/
│   └── Flutter mobile app
│
├── docs/
│   └── Project documentation
│
├── scripts/
│   └── Helper scripts for setup, seeding, and development
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 3. Full Recommended Structure

```txt
campus-shuttle-tracker/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── driver.py
│   │   │   │   │   ├── student.py
│   │   │   │   │   ├── trips.py
│   │   │   │   │   ├── routes.py
│   │   │   │   │   ├── stops.py
│   │   │   │   │   ├── shuttles.py
│   │   │   │   │   ├── timetable.py
│   │   │   │   │   └── notifications.py
│   │   │   │   │
│   │   │   │   └── router.py
│   │   │   │
│   │   │   └── deps.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── permissions.py
│   │   │   └── constants.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── driver.py
│   │   │   ├── shuttle.py
│   │   │   ├── stop.py
│   │   │   ├── route.py
│   │   │   ├── route_stop.py
│   │   │   ├── trip.py
│   │   │   ├── location_ping.py
│   │   │   ├── subscription.py
│   │   │   ├── timetable.py
│   │   │   └── announcement.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── driver.py
│   │   │   ├── shuttle.py
│   │   │   ├── stop.py
│   │   │   ├── route.py
│   │   │   ├── trip.py
│   │   │   ├── location.py
│   │   │   ├── timetable.py
│   │   │   └── notification.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── trip_service.py
│   │   │   ├── location_service.py
│   │   │   ├── eta_service.py
│   │   │   ├── route_service.py
│   │   │   ├── stop_service.py
│   │   │   ├── shuttle_service.py
│   │   │   ├── notification_service.py
│   │   │   └── stale_detection_service.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── driver_repository.py
│   │   │   ├── shuttle_repository.py
│   │   │   ├── stop_repository.py
│   │   │   ├── route_repository.py
│   │   │   ├── trip_repository.py
│   │   │   ├── location_repository.py
│   │   │   └── timetable_repository.py
│   │   │
│   │   ├── utils/
│   │   │   ├── distance.py
│   │   │   ├── datetime.py
│   │   │   ├── responses.py
│   │   │   └── validators.py
│   │   │
│   │   ├── jobs/
│   │   │   ├── stale_trip_checker.py
│   │   │   └── notification_jobs.py
│   │   │
│   │   ├── tests/
│   │   │   ├── test_auth.py
│   │   │   ├── test_trips.py
│   │   │   ├── test_location.py
│   │   │   ├── test_eta.py
│   │   │   └── test_student_live.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── Dockerfile
│   └── README.md
│
├── mobile/
│   ├── shuttle_app/
│   │   ├── lib/
│   │   │   ├── main.dart
│   │   │   ├── app.dart
│   │   │   │
│   │   │   ├── core/
│   │   │   │   ├── config/
│   │   │   │   │   ├── app_config.dart
│   │   │   │   │   └── environment.dart
│   │   │   │   │
│   │   │   │   ├── constants/
│   │   │   │   │   ├── app_colors.dart
│   │   │   │   │   ├── app_routes.dart
│   │   │   │   │   └── api_endpoints.dart
│   │   │   │   │
│   │   │   │   ├── networking/
│   │   │   │   │   ├── api_client.dart
│   │   │   │   │   ├── api_exception.dart
│   │   │   │   │   └── auth_interceptor.dart
│   │   │   │   │
│   │   │   │   ├── storage/
│   │   │   │   │   ├── secure_storage_service.dart
│   │   │   │   │   └── local_storage_service.dart
│   │   │   │   │
│   │   │   │   ├── location/
│   │   │   │   │   ├── location_permission_service.dart
│   │   │   │   │   ├── location_tracking_service.dart
│   │   │   │   │   └── background_location_service.dart
│   │   │   │   │
│   │   │   │   └── utils/
│   │   │   │       ├── date_formatter.dart
│   │   │   │       └── validators.dart
│   │   │   │
│   │   │   ├── shared/
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── primary_button.dart
│   │   │   │   │   ├── loading_view.dart
│   │   │   │   │   ├── error_view.dart
│   │   │   │   │   └── status_badge.dart
│   │   │   │   │
│   │   │   │   └── models/
│   │   │   │       ├── stop_model.dart
│   │   │   │       ├── route_model.dart
│   │   │   │       ├── shuttle_model.dart
│   │   │   │       ├── trip_model.dart
│   │   │   │       └── live_trip_model.dart
│   │   │   │
│   │   │   ├── features/
│   │   │   │   ├── auth/
│   │   │   │   │   ├── data/
│   │   │   │   │   │   ├── auth_api.dart
│   │   │   │   │   │   └── auth_repository.dart
│   │   │   │   │   ├── presentation/
│   │   │   │   │   │   ├── login_screen.dart
│   │   │   │   │   │   └── widgets/
│   │   │   │   │   └── state/
│   │   │   │   │       └── auth_controller.dart
│   │   │   │   │
│   │   │   │   ├── student_live/
│   │   │   │   │   ├── data/
│   │   │   │   │   │   ├── student_live_api.dart
│   │   │   │   │   │   └── student_live_repository.dart
│   │   │   │   │   ├── presentation/
│   │   │   │   │   │   ├── live_map_screen.dart
│   │   │   │   │   │   ├── timetable_screen.dart
│   │   │   │   │   │   └── widgets/
│   │   │   │   │   │       ├── shuttle_status_card.dart
│   │   │   │   │   │       ├── eta_card.dart
│   │   │   │   │   │       ├── next_stop_card.dart
│   │   │   │   │   │       └── map_marker_widgets.dart
│   │   │   │   │   └── state/
│   │   │   │   │       └── student_live_controller.dart
│   │   │   │   │
│   │   │   │   ├── driver_trip/
│   │   │   │   │   ├── data/
│   │   │   │   │   │   ├── driver_trip_api.dart
│   │   │   │   │   │   └── driver_trip_repository.dart
│   │   │   │   │   ├── presentation/
│   │   │   │   │   │   ├── driver_home_screen.dart
│   │   │   │   │   │   ├── start_trip_screen.dart
│   │   │   │   │   │   ├── active_trip_screen.dart
│   │   │   │   │   │   └── widgets/
│   │   │   │   │   │       ├── start_trip_button.dart
│   │   │   │   │   │       ├── end_trip_button.dart
│   │   │   │   │   │       ├── change_next_stop_sheet.dart
│   │   │   │   │   │       └── delay_cancel_controls.dart
│   │   │   │   │   └── state/
│   │   │   │   │       └── driver_trip_controller.dart
│   │   │   │   │
│   │   │   │   ├── notifications/
│   │   │   │   │   ├── data/
│   │   │   │   │   │   ├── notification_api.dart
│   │   │   │   │   │   └── notification_repository.dart
│   │   │   │   │   ├── presentation/
│   │   │   │   │   │   └── notification_settings_screen.dart
│   │   │   │   │   └── state/
│   │   │   │   │       └── notification_controller.dart
│   │   │   │   │
│   │   │   │   └── profile/
│   │   │   │       ├── data/
│   │   │   │       ├── presentation/
│   │   │   │       └── state/
│   │   │   │
│   │   │   └── router/
│   │   │       └── app_router.dart
│   │   │
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── map/
│   │   │
│   │   ├── test/
│   │   ├── pubspec.yaml
│   │   └── README.md
│   │
│   └── README.md
│
├── docs/
│   ├── projectdescription.md
│   ├── projectoverview.md
│   ├── systemdescription.md
│   ├── architecture.md
│   ├── databasedesign.md
│   ├── folderstructure.md
│   └── todo.md
│
├── scripts/
│   ├── seed_data.py
│   ├── reset_db.py
│   └── create_test_trip.py
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 4. Backend Folder Explanation

## 4.1 `backend/app/api/`

This folder contains API routes.

```txt
api/
├── v1/
│   ├── endpoints/
│   └── router.py
└── deps.py
```

### Purpose

This keeps your API endpoints organized by feature.

Examples:

```txt
driver.py      → driver trip actions
student.py     → public student shuttle views
trips.py       → trip-related APIs
routes.py      → route APIs
stops.py       → stop APIs
shuttles.py    → shuttle APIs
```

The endpoint files should stay thin. They should mostly:

1. Receive the request.
2. Validate permissions.
3. Call the correct service.
4. Return a response.

The heavy logic should not live inside endpoint files.

---

## 4.2 `backend/app/core/`

This folder stores global app settings and security logic.

```txt
core/
├── config.py
├── security.py
├── permissions.py
└── constants.py
```

### Purpose

Use this folder for:

- Environment variables
- JWT settings
- Password hashing
- Role permissions
- App constants
- Status values

Example:

```txt
TRIP_STATUS_ACTIVE = "active"
TRIP_STATUS_COMPLETED = "completed"
DEFAULT_AVERAGE_SPEED_MPH = 20
STALE_LOCATION_SECONDS = 60
OFFLINE_LOCATION_SECONDS = 300
```

---

## 4.3 `backend/app/db/`

This folder manages database and Redis connections.

```txt
db/
├── database.py
├── redis.py
├── base.py
└── session.py
```

### Purpose

Use this folder for:

- PostgreSQL connection
- SQLAlchemy/SQLModel setup
- Redis connection
- Database session dependency
- Model base imports for Alembic

---

## 4.4 `backend/app/models/`

This folder contains database models.

```txt
models/
├── user.py
├── driver.py
├── shuttle.py
├── stop.py
├── route.py
├── route_stop.py
├── trip.py
├── location_ping.py
├── subscription.py
├── timetable.py
└── announcement.py
```

### Purpose

Each file should represent a database table or closely related table group.

Example:

```txt
trip.py = trips table
location_ping.py = location_pings table
stop.py = stops table
```

---

## 4.5 `backend/app/schemas/`

This folder contains Pydantic schemas for request and response validation.

```txt
schemas/
├── auth.py
├── user.py
├── driver.py
├── shuttle.py
├── stop.py
├── route.py
├── trip.py
├── location.py
├── timetable.py
└── notification.py
```

### Purpose

Schemas define what data the API accepts and returns.

Example:

```python
class LocationPingCreate(BaseModel):
    latitude: float
    longitude: float
    speed_mph: float | None = None
    heading: float | None = None
```

---

## 4.6 `backend/app/services/`

This folder contains the main business logic.

```txt
services/
├── auth_service.py
├── trip_service.py
├── location_service.py
├── eta_service.py
├── route_service.py
├── stop_service.py
├── shuttle_service.py
├── notification_service.py
└── stale_detection_service.py
```

### Purpose

This is one of the most important backend folders.

Examples:

```txt
trip_service.py
- start trip
- end trip
- change next stop
- cancel trip
- report delay

location_service.py
- receive GPS ping
- save location history
- update Redis live state

eta_service.py
- calculate distance
- calculate ETA
- smooth speed values

stale_detection_service.py
- detect stale shuttle GPS
- mark shuttle offline
```

---

## 4.7 `backend/app/repositories/`

This folder handles direct database queries.

```txt
repositories/
├── user_repository.py
├── driver_repository.py
├── shuttle_repository.py
├── stop_repository.py
├── route_repository.py
├── trip_repository.py
├── location_repository.py
└── timetable_repository.py
```

### Purpose

Repositories separate database operations from business logic.

Example:

```txt
trip_service.py should decide what should happen.
trip_repository.py should handle the database query.
```

This keeps the backend cleaner as the system grows.

---

## 4.8 `backend/app/utils/`

This folder contains reusable helper functions.

```txt
utils/
├── distance.py
├── datetime.py
├── responses.py
└── validators.py
```

### Purpose

Use this folder for logic that does not belong to one specific feature.

Examples:

- Haversine distance formula
- Time formatting
- API response helpers
- Latitude/longitude validators

---

## 4.9 `backend/app/jobs/`

This folder contains background jobs or scheduled checks.

```txt
jobs/
├── stale_trip_checker.py
└── notification_jobs.py
```

### Purpose

Use this folder for tasks that run in the background.

Examples:

- Check if shuttle GPS is stale.
- Mark shuttle offline.
- Send notifications.
- Clean old Redis keys.

For MVP, this can be simple. Later, you can use Celery, RQ, APScheduler, or another background job system.

---

## 5. Flutter Mobile Folder Explanation

For now, it is better to build **one Flutter app with student mode and driver mode** unless you specifically want separate apps.

Recommended:

```txt
mobile/shuttle_app/
```

Why one app first?

- Easier to manage.
- Shared API client.
- Shared models.
- Shared design system.
- Shared map setup.
- Easier development for MVP.

Later, you can split it into:

```txt
student_app/
driver_app/
```

if the system grows.

---

## 5.1 `mobile/shuttle_app/lib/core/`

This contains app-wide services and configuration.

```txt
core/
├── config/
├── constants/
├── networking/
├── storage/
├── location/
└── utils/
```

### Purpose

Use this folder for:

- API base URL
- Environment configuration
- App colors
- Route names
- HTTP client
- Secure storage
- Location permission handling
- Background location tracking

---

## 5.2 `mobile/shuttle_app/lib/shared/`

This contains reusable widgets and models.

```txt
shared/
├── widgets/
└── models/
```

### Purpose

Use this for things used by multiple features.

Examples:

- Buttons
- Loading screens
- Error screens
- Status badges
- Trip model
- Stop model
- Shuttle model

---

## 5.3 `mobile/shuttle_app/lib/features/`

This is where the main app features live.

```txt
features/
├── auth/
├── student_live/
├── driver_trip/
├── notifications/
└── profile/
```

Each feature should have:

```txt
data/
presentation/
state/
```

### Feature Folder Pattern

```txt
feature_name/
├── data/
│   ├── feature_api.dart
│   └── feature_repository.dart
│
├── presentation/
│   ├── feature_screen.dart
│   └── widgets/
│
└── state/
    └── feature_controller.dart
```

### Purpose

This keeps the Flutter app clean and scalable.

---

## 5.4 `student_live/`

This feature handles the student-facing shuttle tracking experience.

```txt
student_live/
├── data/
│   ├── student_live_api.dart
│   └── student_live_repository.dart
├── presentation/
│   ├── live_map_screen.dart
│   ├── timetable_screen.dart
│   └── widgets/
│       ├── shuttle_status_card.dart
│       ├── eta_card.dart
│       ├── next_stop_card.dart
│       └── map_marker_widgets.dart
└── state/
    └── student_live_controller.dart
```

### Responsibilities

- Fetch active shuttle.
- Display map.
- Show shuttle marker.
- Show stop markers.
- Show ETA.
- Show next stop.
- Show stale/offline status.
- Refresh live data every few seconds.

---

## 5.5 `driver_trip/`

This feature handles driver trip control and GPS sending.

```txt
driver_trip/
├── data/
│   ├── driver_trip_api.dart
│   └── driver_trip_repository.dart
├── presentation/
│   ├── driver_home_screen.dart
│   ├── start_trip_screen.dart
│   ├── active_trip_screen.dart
│   └── widgets/
│       ├── start_trip_button.dart
│       ├── end_trip_button.dart
│       ├── change_next_stop_sheet.dart
│       └── delay_cancel_controls.dart
└── state/
    └── driver_trip_controller.dart
```

### Responsibilities

- Start trip.
- End trip.
- Send GPS location.
- Change next stop.
- Report delay.
- Cancel trip.
- Show GPS status.
- Handle location permissions.

---

## 6. Recommended Backend Module Responsibilities

## `trip_service.py`

Responsible for:

- Starting a trip
- Ending a trip
- Cancelling a trip
- Reporting a delay
- Updating next stop
- Updating trip status

## `location_service.py`

Responsible for:

- Receiving GPS pings
- Validating active trip
- Saving ping to PostgreSQL
- Updating latest location in Redis
- Updating last ping timestamp

## `eta_service.py`

Responsible for:

- Calculating distance
- Calculating ETA
- Calculating speed from GPS points
- Smoothing speed values
- Falling back to default speed

## `stale_detection_service.py`

Responsible for:

- Checking last GPS ping time
- Marking location as stale
- Marking trip as offline
- Restoring active status when GPS resumes

## `notification_service.py`

Responsible for:

- Sending push notifications
- Notifying students when shuttle starts
- Notifying students when shuttle is near preferred stop
- Notifying delay/cancellation events

---

## 7. Recommended API File Responsibilities

## `driver.py`

Driver-specific actions:

```txt
POST   /driver/trips/start
POST   /driver/trips/{trip_id}/location
PATCH  /driver/trips/{trip_id}/next-stop
PATCH  /driver/trips/{trip_id}/delay
PATCH  /driver/trips/{trip_id}/cancel
POST   /driver/trips/{trip_id}/end
```

## `student.py`

Student-facing public and student account actions:

```txt
GET    /student/shuttles/active
GET    /student/trips/{trip_id}/live
GET    /student/routes
GET    /student/timetable
POST   /student/subscriptions
DELETE /student/subscriptions/{subscription_id}
```

## `routes.py`

Route management and route display:

```txt
GET    /routes
GET    /routes/{route_id}
```

## `stops.py`

Stop display and stop details:

```txt
GET    /stops
GET    /stops/{stop_id}
```

---

## 8. Environment Variables

Recommended `.env.example`:

```env
APP_NAME=Campus Shuttle Tracking System
APP_ENV=development
APP_DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/campus_shuttle
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

DEFAULT_AVERAGE_SPEED_MPH=20
STALE_LOCATION_SECONDS=60
OFFLINE_LOCATION_SECONDS=300

FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=

MAP_PROVIDER=google
GOOGLE_MAPS_API_KEY=
MAPBOX_ACCESS_TOKEN=
```

---

## 9. Docker Compose Structure

For local development:

```txt
docker-compose.yml
```

Should run:

```txt
PostgreSQL + PostGIS
Redis
Backend API
```

Example services:

```txt
services:
  postgres:
  redis:
  backend:
```

The Flutter app can run separately from the local machine or emulator.

---

## 10. Why This Structure Is Good

This structure is good because it separates responsibilities clearly.

```txt
api/ = request and response layer
services/ = business logic
repositories/ = database queries
models/ = database tables
schemas/ = request/response validation
db/ = database and Redis connections
core/ = app settings and security
utils/ = reusable helper functions
jobs/ = background tasks
```

For Flutter:

```txt
core/ = app-wide setup
shared/ = reusable widgets/models
features/ = main app features
data/ = API/repository
presentation/ = screens/widgets
state/ = controllers/state management
```

This makes the project easier to build, debug, test, and scale.

---

## 11. MVP Build Priority

Do not build every folder fully from day one.

Start with this smaller structure:

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

mobile/shuttle_app/lib/
├── core/
├── shared/
├── features/
└── main.dart
```

Then add repositories, jobs, tests, and more advanced modules as the project grows.

---

## 12. Final Recommendation

For the current stage, focus on these parts first:

```txt
backend/app/models/
backend/app/schemas/
backend/app/services/trip_service.py
backend/app/services/location_service.py
backend/app/services/eta_service.py
backend/app/api/v1/endpoints/driver.py
backend/app/api/v1/endpoints/student.py

mobile/shuttle_app/lib/features/driver_trip/
mobile/shuttle_app/lib/features/student_live/
mobile/shuttle_app/lib/core/location/
mobile/shuttle_app/lib/core/networking/
```

The core system should be built before the admin dashboard.

The most important early success is:

```txt
Driver app starts trip and sends GPS.
Student app sees shuttle live with ETA and next stop.
```
