import logging
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

from src.bot.states import *
from .start import start_function_command, skip_function
from .menu_handlers import handle_text_command_selection
from src.bot.commands.text_generation.handlers import handle_text_generation_messages

from src.bot.commands.info_of_nko.collection_info.collection_info import collection_info

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
            CommandHandler("plan", handle_text_command_selection)
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
    if command in ["/start", "/main_menu", "/skip", "/text_generation", "/image_generator", "/correct_text", "/plan"]:
        return  # Уже обрабатывается

    await update.message.reply_text("Команда не распознана")
