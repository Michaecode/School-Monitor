"""School Monitor entry point."""

import asyncio
import logging
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from clickedu import ClickeduClient
from config import load_config
from telegram_bot import send_report

BASE_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format=BASE_LOG_FORMAT)


def current_school_week(timezone_name: str) -> tuple[date, date]:
    today = date.today()
    # Monday-Friday of the current week.
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=4)


async def main() -> None:
    configure_logging()
    logger = logging.getLogger("school_monitor")
    config = load_config()

    settings = config["settings"]
    timezone_name = settings.get("timezone", "Europe/Madrid")
    # Validate the configured timezone before doing any work.
    ZoneInfo(timezone_name)

    start, end = current_school_week(timezone_name)
    clickedu = ClickeduClient(
        url=config["clickedu"]["url"],
        username=config["clickedu"]["username"],
        password=config["clickedu"]["password"],
        headless=settings.getboolean("headless", fallback=True),
    )

    logger.info("Starting attendance check for %s to %s", start, end)
    absences = await clickedu.fetch_absences(start, end)

    # Sending is intentionally reached only after a real extraction succeeds.
    from attendance import format_weekly_report

    message = format_weekly_report(absences, start, end)
    await send_report(
        token=config["telegram"]["bot_token"],
        chat_id=config["telegram"]["chat_id"],
        message=message,
    )
    logger.info("Weekly report sent.")


if __name__ == "__main__":
    asyncio.run(main())
