---
slug: meetings
number: "07"
part: "2"
lang: en
title: "Meetings and Booking on Your Own Side — Jitsi and Cal.com"
subtitle: "Teams meetings, Calendly booking, and webinars for classes — on your own domain"
description: Video meetings with Jitsi, booking with Cal.com, classes and webinars with BigBlueButton. Replace Teams, Zoom, Calendly, and Microsoft Bookings with your own domain on your own server. Booking rides on the PostgreSQL from Chapter 2 and sends confirmations through the Chapter 6 mail. Step off per-seat, per-minute billing and keep meeting links and records on your own side.
date: 2026.07.11
label: Independence 7
title_html: Meetings and booking,<br>on <span class="accent">your own domain</span>.
prev_slug: mail
prev_title: "Mail on Your Own Side — Stalwart and Thunderbird"
next_slug: web
next_title: "Publish the Web — Cloudflare Pages (a WordPress Replacement)"
---

# Meetings and Booking on Your Own Side — Jitsi and Cal.com

Meetings and booking are generic functions. Teams calls, Calendly scheduling,
Microsoft Bookings for course reservations — all of it is already shared as
OSS. Here we stand up three and place them on your own domain.

- **Video meetings** — Jitsi Meet (in place of Teams and Zoom)
- **Booking** — Cal.com (in place of Calendly and Bookings)
- **Classes and webinars** — BigBlueButton (for larger teaching sessions)

## Stand up Jitsi Meet

For small-to-mid meetings, **Jitsi Meet.** Participants need **only a
browser** — no app install, no account. Send a link and the meeting starts.

```bash
# use the official compose bundle
git clone https://github.com/jitsi/docker-jitsi-meet
cd docker-jitsi-meet && cp env.example .env && ./gen-passwords.sh
docker compose up -d        # web, prosody, jicofo, jvb come up
```

Hand out `meet.example.com` with your own logo and domain. Recording, chat, and
screen sharing all come standard.

> Large meetings (hundreds) are handled by adding video bridges (JVB). That is
> "adding" more than "standing up" — lining up servers to match scale.

## Classes — BigBlueButton

Where you need a **whiteboard, raise-hand, breakout rooms, and attendance** —
seminars and lessons — use **BigBlueButton.** A webinar platform built for
education, the tool for the "courses" mentioned back in Chapter 2.

BigBlueButton has its own installer and is heavier than Jitsi. **Day-to-day
meetings on Jitsi, classes on BigBlueButton** — stand each up for its purpose.

## Booking — Cal.com

Scheduling and course booking are **Cal.com,** a replacement for Calendly and
Microsoft Bookings, with data on the **PostgreSQL from Chapter 2.**

```yaml
# compose.yaml — stand up booking on the Chapter 2 DB
services:
  booking:
    image: calcom/cal.com:latest
    environment:
      DATABASE_URL: postgres://postgres:change-me@db:5432/calcom
      NEXT_PUBLIC_WEBAPP_URL: https://book.example.com
    restart: always
```

When a booking lands, the **Chapter 6 mail** sends a confirmation and a
day-before reminder, with the Jitsi meeting link attached automatically. On top
of the **foundation (DB), gate (auth), and mail,** booking just sits — what was
laid first pays off here.

## Calendar and the gate

Schedule sync is **CalDAV** (stand up a lightweight Radicale),
connecting to Thunderbird and the stock phone calendar. Cal.com and each app sit
behind the Chapter 3 gate, beyond the reverse proxy.

```caddy
meet.example.com { reverse_proxy jitsi-web:80 }
book.example.com { reverse_proxy booking:3000 }
```

## Summary

Meetings and booking, on your own domain.

- **Jitsi Meet** — browser-only meetings, in place of Teams and Zoom
- **BigBlueButton** — classes and webinars with whiteboard and attendance
- **Cal.com** — in place of Calendly and Bookings (on the Chapter 2 PostgreSQL)
- **Integration** — booking → confirmation via Chapter 6 mail, Jitsi link auto-attached
- **CalDAV + gate** — sync with stock calendars, behind the reverse proxy

By now the foundation, gate, documents, code, mail, meetings, and booking are
in place. Next, we **build the website** that shows these to the
outside.

---

## Related articles

- [Chapter 2: Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars](/en/ai-native-ways/software/foundation/)
- [Chapter 6: Mail on Your Own Side — Stalwart and Thunderbird](/en/ai-native-ways/software/mail/)
- [Chapter 1: Becoming Independent from Microsoft and Google — The Whole Map](/en/ai-native-ways/software/independence/)
