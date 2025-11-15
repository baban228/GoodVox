from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from src.bot.states import StateType

from src.bot.commands.settings.Info_settings import info_setting


async def settings_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    # Получаем текущие настройки
    current_role = info_setting.get_role(user_id)
    current_want = info_setting.get_what_you_want(user_id)

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
вот ваши текущие настройки:

🎭 Роль ИИ: {current_role}
🎯 Цель: {current_want}

Выберите, что хотите изменить:
/set_role - сменить роль (роль - это кем представляет себя ии)
/set_what_you_want - сменить цель (как ты хочешь чтоб выводила ответ ии)
"""


    await update.message.reply_text(commands_text)

    return StateType.SETTINGS


