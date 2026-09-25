# Lessons Learned - secure-this
General rules derived from failure patterns. Read at start of every run.

---

## Rule: a snapshot audit expires
**Pattern:** an audit that passes today says nothing about tomorrow. Dependencies
update silently (rug pull), and platform controls change.
**Rule:** every report states when the snapshot expires and what invalidates it.
Never present a verdict as permanent.
**Added:** 2026-08-19 (built in at v1.0, from the design discussion rather than a failure)
