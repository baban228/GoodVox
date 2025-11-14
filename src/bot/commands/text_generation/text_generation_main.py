from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from src.bot.states import *


async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Отправляем сообщение о разработке
    await update.message.reply_text("⚠️ Данная функция все еще в разработке...")


    return StateType.TEXT_GEN