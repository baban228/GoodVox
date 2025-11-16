from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
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
from .start import start_function_command, skip_function
from .menu_handlers import handle_text_command_selection

from src.bot.commands.info_of_nko.collection_info.collection_info import collection_info
from src.bot.commands.info_of_nko.correct_info.correct_info_nko import *

from src.bot.commands.settings.main import *
from src.bot.commands.settings.handlers import *

from src.bot.commands.image_generator.main import *

logger = logging.getLogger(__name__)


def setup_handlers(app):
    conv_handler = ConversationHandler(
        #тут функции новые записываются это не трогать особо
        entry_points=[
            CommandHandler("start", start_function_command),
            CommandHandler("skip", skip_function),
            CommandHandler("text_generation", handle_text_command_selection),
            CommandHandler("image_generator", handle_text_command_selection),
            CommandHandler("correct_text", handle_text_command_selection),
            CommandHandler("plan", handle_text_command_selection),
            CommandHandler("correct_info_nko", handle_text_command_selection),

            CommandHandler("settings", settings_info),
            CommandHandler("set_role", handler_settings_text_command),
            CommandHandler("set_what_you_want", handler_settings_text_command),
            CommandHandler("close_settings", handler_settings_text_command),

            CommandHandler("get_nko", show_current_info),
            CommandHandler("remove_all_nko", remove_all_nko),
            CommandHandler("remove_last_nko", remove_last_nko)
        ],
        #тут состояния, тип пока скажем MAIN_MENU будет вызываться всегда handle_text_command_selection, чтоб новое
        # добавить просто скопируй и замени на свои данные
        states={
            StateType.COLL_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, collection_info),
            ],
            StateType.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_command_selection),
            ],
            StateType.SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings_messages),
            ],
            StateType.IMAGE_GEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, generation_image),
            ]
        },
        fallbacks=[CommandHandler("start", start_function_command)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.COMMAND, handle_commands))


async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):

    command = update.message.text.split()[0]
    '''Короч сюда записываем новые функции, тут тип они ищутся'''
    if command in ["/start", "/skip", "/text_generation", "/image_generator", "/correct_text", "/plan", "/correct_info_nko", "/settings",
                   "/get_nko", "remove_all_nko", "remove_last_nko",
                   "set_role", "/set_what_you_want", "close_settings"]:
        return  # Уже обрабатывается

    await update.message.reply_text("Команда не распознана")