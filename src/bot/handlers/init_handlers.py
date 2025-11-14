from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from .start import start_command
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

from src.bot.states import *
from .start import start_command
from .menu_handlers import handle_text_command_selection

logger = logging.getLogger(__name__)


def setup_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    conv_handler = ConversationHandler(
        #тут функции новые записываются это не трогать особо
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("text_generation", handle_text_command_selection),
            CommandHandler("image_generator", handle_text_command_selection),
            CommandHandler("correct_text", handle_text_command_selection),
            CommandHandler("plan", handle_text_command_selection)
        ],
        #тут состояния, тип пока скажем MAIN_MENU будет вызываться всегда handle_text_command_selection, чтоб новое
        # добавить просто скопируй и замени на свои данные
        states={
            StateType.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_command_selection),
            ]
        },
        fallbacks=[CommandHandler("start", start_command)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.COMMAND, handle_commands))


async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):

    command = update.message.text.split()[0]
    '''Короч сюда записываем новые функции, тут тип они ищутся'''
    if command in ["/start", "/text_generation", "/image_generator", "/correct_text", "/plan"]:
        return  # Уже обрабатывается

    await update.message.reply_text("Команда не распознана")