# RoomBooking API — Brief

RoomBooking API. Rooms (name, capacity). Bookings (roomId, start, end as UTC DateTime, bookedBy).

**Endpoints:** rooms CRUD (4), `POST /api/bookings`, `GET /api/rooms/{id}/bookings?date=`, `DELETE /api/bookings/{id}`.

**Invariant:** bookings for the same room never overlap, including under concurrent requests.

**Stretch (optional):** a background service releases bookings not confirmed within 15 minutes.

**Out of scope:** auth, UI, notifications.

**Stack:** .NET 8, ASP.NET Core, EF Core + SQLite, xUnit.

**Harness first:** no feature code before the harness commit.
