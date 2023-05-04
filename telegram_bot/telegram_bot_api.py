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


async def _send_img(img):
    bot = telegram.Bot(settings.TELEGRAM_BOT_TOKEN)
    async with bot:
        await bot.send_photo(907681435, photo=img)

def send_img(img):
    asyncio.run(_send_img(img))