import logging
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

from .start import start_function_command, skip_function
from .menu_handlers import handle_text_command_selection
from src.bot.commands.text_generation.handlers import handle_text_generation_messages

from src.bot.commands.info_of_nko.collection_info.collection_info import collection_info

from src.bot.commands.info_of_nko.correct_info.correct_info_nko import *
from src.bot.commands.settings.handlers import *
logger = logging.getLogger(__name__)


def setup_handlers(app):
    conv_handler = ConversationHandler(
        #функции констекстного меню с обработчиками
        entry_points=[
            CommandHandler("start", start_function_command),
            CommandHandler("main_menu", start_function_command),
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
        #состояния, MAIN_MENU будет всегда вызывать handle_text_command_selection
        #               TEXT_GEN вызывает hand
        states={
            StateType.COLL_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, collection_info),
            ],
            StateType.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_command_selection),
            ],
            StateType.TEXT_GEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_generation_messages),
            ],
            StateType.SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings_messages),
            ]
        },
        fallbacks=[CommandHandler("start", start_function_command)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.COMMAND, handle_commands))


async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):

    command = update.message.text.split()[0]
    '''Сюда записываем новые функции, тут они ищутся'''
    if command in ["/start", "/main_menu", "/skip", "/text_generation", "/image_generator", "/correct_text", "/plan", "/correct_info_nko", "/settings",
                   "/get_nko", "remove_all_nko", "remove_last_nko",
                   "set_role", "/set_what_you_want", "close_settings"]:
        return  # Уже обрабатывается

    await update.message.reply_text("Команда не распознана")