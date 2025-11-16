from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from src.bot.states import StateType

from src.bot.commands.settings.Info_settings import info_setting

async def set_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    response_text = """🎭 Введите новую роль ИИ (как вы хотите, чтобы ИИ представлял себя):"""

    await update.message.reply_text(response_text)
    context.user_data['waiting_for'] = 'role'
    return StateType.SETTINGS


async def set_what_you_want(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /set_what_you_want"""

    response_text = f"""🎯 {update.effective_user.first_name or 'Пользователь'}, 
введите новую цель (как вы хотите, чтобы ИИ отвечал):
"""

    await update.message.reply_text(response_text)
    context.user_data['waiting_for'] = 'want'
    return StateType.SETTINGS
