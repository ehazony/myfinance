from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import telegram_bot.telegram_bot_api

BOT_TOKEN = "5329467010:AAHxFZ1czZGrHg7mR8c3I6yprVAQkZlKE3M"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.telegram_bot_api.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot.telegram_bot_api.send_message(chat_id=update.effective_chat.id, text=update.message.text)


class Command(BaseCommand):

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def handle(self, *args, **options):
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        start_handler = CommandHandler('start', start)

        application.add_handler(start_handler)
        application.add_handler(echo_handler)

        application.run_polling()
        # efraim = User.objects.get(username='efraim')
