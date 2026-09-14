from datetime import datetime, timedelta

from django.utils import timezone


def _escape_ics_text(value):
    """
    Escapes text per RFC 5545 for safe inclusion in an .ics file.
    Commas, semicolons, backslashes, and newlines all have special
    meaning in the ICS format, unescaped values could corrupt the
    file or bleed into the wrong calendar field.
    """
    if not value:
        return ""
    value = value.replace("\\", "\\\\")
    value = value.replace(";", "\\;")
    value = value.replace(",", "\\,")
    value = value.replace("\n", "\\n")
    return value


def _format_ics_datetime(dt):
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_event_ics(event):
    """
    Builds a minimal, valid RFC 5545 .ics file for a single Event.
    Stdlib only, no new dependency. Defaults to a 1-hour duration
    when end_time is not set, matching common calendar-app behavior.
    """
    start_dt = datetime.combine(event.event_date, event.start_time)
    if event.end_time:
        end_dt = datetime.combine(event.event_date, event.end_time)
    else:
        end_dt = start_dt + timedelta(hours=1)

    uid = f"event-{event.pk}@church-cms"
    now_stamp = _format_ics_datetime(timezone.now())

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Church CMS//Event//EN",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{now_stamp}",
        f"DTSTART:{_format_ics_datetime(start_dt)}",
        f"DTEND:{_format_ics_datetime(end_dt)}",
        f"SUMMARY:{_escape_ics_text(event.title)}",
    ]
    if event.description:
        lines.append(f"DESCRIPTION:{_escape_ics_text(event.description)}")
    if event.location:
        lines.append(f"LOCATION:{_escape_ics_text(event.location)}")
    lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")

    return "\r\n".join(lines) + "\r\n"