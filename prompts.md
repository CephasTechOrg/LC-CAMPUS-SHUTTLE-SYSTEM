# CloudDesign Guided Prompt — Campus Shuttle Tracking App Mockups

## How to Use This Prompt

Upload the generated mockup images together with this prompt into CloudDesign.

Use the images as the **visual reference** and this prompt as the **design and implementation guide**.

The goal is to recreate the same professional mobile UI design for a real-time campus shuttle tracking system.

---

# Master Prompt

You are designing a high-fidelity mobile app interface for a **Campus Shuttle Tracking System**.

The app helps students and drivers track the campus shuttle in real time. The design should be modern, professional, clean, and transport-tech focused.

Use the attached mockup images as the main visual reference. Recreate the same design system, layout quality, spacing, colors, typography, cards, icons, map sections, buttons, and mobile structure.

The app should feel like a polished production-ready mobile product, not a rough prototype.

The design should support two main user groups:

1. **Students**
   - View live shuttle location
   - See next stop
   - See ETA
   - View route details
   - View timetable
   - Manage alerts and preferred stop
   - Continue as guest without login for public tracking

2. **Drivers**
   - Login
   - Select shuttle
   - Select route
   - Start trip
   - Send GPS tracking
   - Change next stop
   - Report delay
   - End trip

Do not focus on the admin dashboard for now. Focus on the student and driver mobile experience.

---

# Design Style

## Overall Visual Direction

Use a premium, clean, modern mobile UI style.

The app should look like a professional campus mobility product with:

- Dark navy header areas
- White rounded cards
- Teal/emerald accent actions
- Soft gray background
- Light map UI
- Clean icons
- Large readable text
- Rounded corners
- Soft shadows
- Smooth spacing
- Bottom navigation
- Modern iPhone-style mobile layout

The design should feel trustworthy, calm, and easy to use.

---

# Color Palette

Use a consistent color palette across every screen.

## Primary Colors

```txt
Deep Navy: #061B3A
Dark Navy: #082B52
Teal/Emerald Accent: #009E8E
Bright Teal: #14B8A6
White: #FFFFFF
Light Background: #F6F8FB
Card Border: #E5EAF0
Muted Text: #667085
Dark Text: #0B1F3A
```

## Status Colors

```txt
Active / Success: #009E8E
Scheduled / Info: #2F80ED
Warning / Delay: #F59E0B
Danger / Cancel / End Trip: #EF4444
Offline / Muted: #98A2B3
```

Use amber only for warnings and alerts. Use red only for destructive actions such as **End Trip** or **Cancelled**.

---

# Typography

Use a clean modern sans-serif typeface.

Preferred:

```txt
SF Pro
Inter
Roboto
```

Typography should feel close to iOS design.

Suggested type scale:

```txt
Large Page Title: 28–34px, bold
Section Title: 20–24px, semi-bold
Card Title: 18–22px, semi-bold
Body Text: 14–16px, regular
Small Labels: 12–13px, medium
Button Text: 16–18px, semi-bold
```

Use strong hierarchy. Important data such as ETA should be large and easy to read.

---

# Layout Rules

Use a mobile-first design around an iPhone-style screen size.

Recommended canvas/frame:

```txt
Width: 390px
Height: 844px
```

Follow these spacing rules:

```txt
Screen horizontal padding: 20–24px
Card padding: 16–20px
Card radius: 20–28px
Button radius: 16–20px
Small pill radius: 999px
Spacing between sections: 16–24px
```

Use white cards on light backgrounds. Use dark navy headers where appropriate.

---

# Icon Style

Use clean line icons or filled icons consistently.

Recommended icon categories:

```txt
Bus / shuttle
Map pin
Clock
Calendar
Bell
Warning triangle
User/profile
Route nodes
Building/campus
GPS/target
Chevron arrows
Play/start
Stop/end
```

Icons should feel modern and simple, not cartoonish.

Do not use emoji as icons, except the greeting wave can remain if desired.

---

# Map Style

Map areas are important. The map should look like a soft campus map.

Use:

- Pale green campus zones
- Light gray buildings
- White/light roads
- Soft blue lake/water shapes if needed
- Teal route line
- Direction arrows along route
- Circular stop markers
- Dark navy stop labels
- Teal shuttle marker
- Soft glow around active shuttle marker
- Floating GPS/current-location button

The map does not need to be a real Google/Mapbox map in the mockup. It can be a clean static design placeholder that looks like a map.

---

# Navigation Structure

Use bottom navigation for student-facing screens:

```txt
Home
Routes / Timetable
Alerts
Profile
```

The active tab should use dark navy and teal indicator. Inactive tabs should use gray.

For driver screens, the bottom navigation can remain visually consistent, but the content should focus on driver controls.

---

# Required Screens

Create the following high-fidelity mobile screens.

---

## 1. Login / Welcome Screen

Purpose:

Allow students or drivers to sign in. Students should also be able to continue as guest to view public shuttle tracking.

Content:

```txt
App logo
Title: Campus Shuttle
Subtitle: Live shuttle tracking for a smarter campus commute.
School Email input
Password input
Remember me checkbox
Forgot password link
Primary button: Sign In
Divider: or
Secondary outlined button: Continue as Guest
Helper link: Need help? Contact Transport Office
```

Visual requirements:

- Dark navy top area with shuttle/map illustration
- White rounded bottom sheet form
- Teal primary button
- Outlined teal guest button
- Clean input fields with icons
- Professional and trustworthy layout

---

## 2. Student Live Tracking Home Screen

Purpose:

Main student screen for viewing active shuttle status.

Content:

```txt
Header: Campus Shuttle
Status pill: Active
Greeting: Good morning, Alex!
Subtitle: Track your shuttle in real time.
Notification bell icon
Large live map section
Route loop with stops:
- Main Campus
- Off-Campus Housing
- Sub-Campus
Moving shuttle marker
Bottom sheet card:
- Campus Shuttle 1
- Status: On Route
- Next Stop: Off-Campus Housing
- ETA: 7 min
- Last Updated: 9:41 AM
Quick action cards:
- View Timetable
- Notifications
Bottom navigation
```

Visual requirements:

- Map should be prominent
- Bottom sheet should feel layered above the map
- ETA should be very visible
- Shuttle status should be clear at a glance
- Use teal for active route and shuttle marker

---

## 3. Timetable Screen

Purpose:

Students view today’s and weekly shuttle schedules.

Content:

```txt
Header: Timetable
Search icon
Segmented control: Today / Week
Date selector: Tuesday, May 13
Schedule cards:
1. Main Campus → Off-Campus Housing
   - Departure: 9:15 AM
   - ETA: 12 min
   - Vehicle: Shuttle 1
   - Status: Active
   - Mini route line with 4 stops

2. Main Campus → Sub-Campus
   - Departure: 11:30 AM
   - ETA: 10 min
   - Vehicle: Shuttle 2
   - Status: Scheduled
   - Mini route line with 3 stops

3. Full Loop Route
   - Departure: 2:00 PM
   - ETA: 28 min
   - Vehicle: Shuttle 3
   - Status: Scheduled
   - Mini route line with 7 stops
Bottom navigation
```

Visual requirements:

- Schedule cards should be easy to scan
- Active route badge should be teal
- Scheduled badge should be blue
- Route mini-lines should use teal
- Use strong spacing between cards

---

## 4. Route Details Screen

Purpose:

Students view a specific route and its stops.

Content:

```txt
Header: Route Details
Back button
Route name: Campus Loop
Status: Active
Map preview with route loop
Stops:
- Main Campus
- Off-Campus Housing
- Sub-Campus
Summary chips:
- 3 Stops
- 25 min avg
- Loop Route
Vertical stop timeline:
1. Main Campus
   Departure • 9:41 AM
   Badge: On Time

2. Off-Campus Housing
   Next Stop • 9:49 AM
   Badge: Next Stop

3. Sub-Campus
   Arrival • 9:58 AM
   Badge: On Time
Primary button: Track Active Shuttle
Bottom navigation
```

Visual requirements:

- The next stop should be highlighted with a soft teal background
- Timeline should use numbered circles
- Summary chips should be compact and rounded
- Map preview should match live tracking style

---

## 5. Alerts & Preferences Screen

Purpose:

Students manage notification settings and preferred stop.

Content:

```txt
Header: Alerts & Preferences
Subtitle: Customize your alerts and choose your preferred stop to stay informed about your shuttle.
Preferred Stop selector:
- Off-Campus Housing
Toggle cards:
- Notify when shuttle starts
- Notify when shuttle is near my stop
- Delay alerts
- Cancellation alerts
Minutes before arrival selector:
- 3 min
- 5 min
- 10 min
Primary button: Save Preferences
Bottom navigation
```

Visual requirements:

- Use clear white setting cards
- Toggles should be teal when on
- Selected minute option should be dark navy
- Use icons for each setting
- Keep this screen calm and organized

---

## 6. Driver Console / Start Trip Screen

Purpose:

Driver selects shuttle and route before starting a trip.

Content:

```txt
Header: Driver Console
Status pill: Active
Greeting: Good morning, Alex!
Subtitle: Ready to get your route started?
Notification icon
Assigned Shuttle selector:
- Campus Shuttle 1
Select Route selector:
- Campus Loop Route
Link: View full route
Scheduled Start:
- Today, May 30, 2025
- 9:45 AM
Route Preview:
- Main Campus
- Off-Campus Housing
- Sub-Campus
- show approximate times between stops
GPS status row:
- GPS Ready
- Location permissions are on.
Primary button: Start Trip
```

Visual requirements:

- This screen should feel operational and simple
- Driver should not feel overloaded
- Start Trip button should be large and obvious
- GPS Ready status should be visible before starting

---

## 7. Driver Active Trip Screen

Purpose:

Driver manages an active trip.

Content:

```txt
Header: Active Trip
Status pill: Live
Greeting: Good morning, Alex!
Subtitle: You are currently on an active trip.
Notification icon
Live map with current shuttle location and route
Control panel:
- Campus Shuttle 1
- Status: Tracking On
- Next Stop: Sub-Campus
- ETA: 3 min
- Speed: 18 mph
Controls:
- Change Next Stop
- Report Delay
- End Trip
Trip summary:
- Trip Started: 9:41 AM
- Passengers: 12
- View Live
Bottom navigation
```

Visual requirements:

- The driver control buttons must be visually distinct:
  - Change Next Stop: soft teal
  - Report Delay: amber warning
  - End Trip: red outline or red danger
- The map should still be large, but controls must be easy to reach
- Use clear active/live status indicators

---

# Component System

Please create a reusable component system based on the mockups.

Core components:

```txt
AppHeader
StatusPill
BottomNavigation
MapPreview
LiveMap
ShuttleMarker
StopMarker
RouteLine
BottomSheetCard
InfoMetric
ActionTile
ScheduleCard
RouteTimeline
SettingsToggleCard
PrimaryButton
SecondaryButton
DangerButton
DropdownSelector
InputField
```

The design should feel consistent across every page.

---

# Flutter Implementation Guidance

If CloudDesign is generating Flutter code, use this guidance.

Use clean Flutter architecture:

```txt
lib/
├── main.dart
├── app.dart
├── core/
│   ├── theme/
│   ├── constants/
│   ├── routing/
│   └── widgets/
├── features/
│   ├── auth/
│   ├── student_live/
│   ├── timetable/
│   ├── route_details/
│   ├── alerts/
│   └── driver_trip/
└── shared/
    ├── models/
    └── widgets/
```

Use mock data first. Do not require backend integration at the design stage.

Use Flutter widgets such as:

```txt
Scaffold
SafeArea
Stack
Positioned
Container
Card
ClipRRect
ListView
SingleChildScrollView
BottomNavigationBar
CustomPainter for route lines if needed
```

Suggested packages if needed later:

```txt
google_maps_flutter
mapbox_maps_flutter
flutter_riverpod
go_router
dio
geolocator
firebase_messaging
```

For the design mockup/code stage, the map can be a static styled placeholder. It should still visually look like the attached map mockups.

---

# UX Rules

Follow these rules carefully:

1. Students should be able to view live shuttle tracking without signing in.
2. Login is only needed for notifications, preferred stop, and profile features.
3. Driver screens must be simple and action-focused.
4. The map should not overpower important ETA/status information.
5. ETA and next stop should always be easy to find.
6. Do not use too many colors.
7. Do not use cluttered cards.
8. Do not add unnecessary admin features yet.
9. Keep all screen designs consistent with the attached mockups.
10. Use the same spacing, typography, icon style, and palette across all screens.

---

# Backend-Aware UI Data

The UI should be designed around these real backend response fields:

```json
{
  "trip_id": "uuid",
  "status": "active",
  "shuttle": {
    "id": "uuid",
    "name": "Campus Shuttle 1"
  },
  "latitude": 35.12345,
  "longitude": -80.12345,
  "heading": 90,
  "next_stop": {
    "id": "uuid",
    "name": "Off-Campus Housing",
    "latitude": 35.12888,
    "longitude": -80.12999
  },
  "eta_minutes": 7,
  "last_updated": "9:41 AM",
  "is_location_stale": false,
  "is_offline": false
}
```

Important UI states to design for:

```txt
Active
Scheduled
Delayed
Cancelled
Offline
No active shuttle
Location stale
GPS permission missing
Loading
Error
```

---

# Empty and Error States

Include simple empty/error states if possible.

## No Active Shuttle

Text:

```txt
No shuttle is currently active.
Check the timetable or turn on notifications to know when the next shuttle starts.
```

Action:

```txt
View Timetable
```

## Offline Shuttle

Text:

```txt
Shuttle location is currently unavailable.
Last updated a few minutes ago.
```

Action:

```txt
Refresh
```

## Driver GPS Missing

Text:

```txt
GPS permission is required to start tracking.
```

Action:

```txt
Enable Location
```

---

# Final Output Expected

Create a polished mobile UI mockup/design system with the following screens:

```txt
1. Login / Welcome
2. Student Live Tracking Home
3. Timetable
4. Route Details
5. Alerts & Preferences
6. Driver Console / Start Trip
7. Driver Active Trip
```

All screens must share the same:

```txt
Color palette
Typography
Card style
Icon style
Spacing
Navigation style
Map style
Button style
```

The design should look ready for implementation in Flutter.

The result should be clean enough that a developer can convert it into Flutter screens directly.
