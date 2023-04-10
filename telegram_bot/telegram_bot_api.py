import telegram

from finance import settings
import asyncio


async def _send_message(text):
    bot = telegram.Bot(settings.TELEGRAM_BOT_TOKEN)
    async with bot:
        print(text)
        await bot.send_message(text=text, chat_id=907681435, parse_mode='markdown')


def send_message(text):
    asyncio.run(_send_message(text))