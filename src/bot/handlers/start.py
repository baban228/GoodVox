from telegram import Update
from telegram.ext import ContextTypes

from src.bot.states import StateType, set_user_state


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """может понадобится"""
    #telegram_user_id = update.effective_user.id
    #username = update.effective_user.username or f'user_{telegram_user_id}'
    #first_name = update.effective_user.first_name or 'Unknown User'


    welcome_text = f"""👋 Привет, {update.effective_user.first_name or 'Пользователь'}!

используй текстовые команды:
/text_generation - генерация текста
/image_generator - генерация картинок
/correct_text - редактирование текста
/plan - создание плана
"""

    await update.message.reply_text(welcome_text)

    # Устанавливаем состояние через архитектуру машины состояния
    await set_user_state(update, context, StateType.MAIN_MENU)

    return StateType.MAIN_MENU