"""Telegram delivery."""

from telegram import Bot


async def send_report(token: str, chat_id: str, message: str) -> None:
    async with Bot(token=token) as bot:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="HTML",
        )
