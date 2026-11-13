"""Attendance data model and Telegram-friendly report formatting."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Absence:
    day: date
    description: str
    hours: str | None = None
    status: str | None = None


def format_weekly_report(absences: list[Absence], week_start: date, week_end: date) -> str:
    """Format the records for Telegram. No records are invented."""
    heading = (
        "<b>School Monitor — weekly attendance</b>\n"
        f"Week: {week_start:%d/%m/%Y} – {week_end:%d/%m/%Y}\n"
    )

    if not absences:
        return heading + "\nNo absence records were found for this week."

    lines = [heading, f"\nRecords: <b>{len(absences)}</b>"]
    for item in sorted(absences, key=lambda record: (record.day, record.hours or "")):
        details = f" — {item.hours}" if item.hours else ""
        status = f" ({item.status})" if item.status else ""
        lines.append(
            f"\n• {item.day:%A %d/%m}: {item.description}{details}{status}"
        )

    return "".join(lines)
