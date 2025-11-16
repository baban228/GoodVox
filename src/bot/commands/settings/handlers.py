from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from src.bot.states import StateType

from .setters import *
from .main import *
async def handler_settings_text_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка текстовых команд"""
    command = update.message.text.split()[0]

    if command == "/set_role":
        return await set_role(update, context)
    elif command == "/set_what_you_want":
        return await set_what_you_want(update, context)
    elif command == "/close_settings":
        return await settings_info(update, context)
    else:

        return StateType.SETTINGS

async def handle_settings_messages(update, context):
    user_message = update.message.text.strip()
    user_id = update.effective_user.id

    # Проверяем, не ожидаем ли мы ввод
    user_state = context.user_data.get('waiting_for')

    if user_state == 'role':
        # Обрабатываем ввод новой роли
        new_role = user_message
        info_setting.set_role(user_id, new_role)
        context.user_data['waiting_for'] = None  # Сбрасываем состояние

        response_text = f"""🎭 Роль ИИ успешно изменена на:
    "{new_role}"

    Текущие настройки:
    🎭 Роль ИИ: {info_setting.get_role(user_id)}
    🎯 Цель: {info_setting.get_what_you_want(user_id)}

    Что дальше:
    /set_role - изменить роль снова
    /set_what_you_want - изменить цель
    /close_settings - закрыть настройки
    """

        await update.message.reply_text(response_text)
        return StateType.SETTINGS

    elif user_state == 'want':
        # Обрабатываем ввод новой цели
        new_want = user_message
        info_setting.set_what_you_want(user_id, new_want)
        context.user_data['waiting_for'] = None  # Сбрасываем состояние

        response_text = f"""🎯 Цель успешно изменена на:
    "{new_want}"

    Текущие настройки:
    🎭 Роль ИИ: {info_setting.get_role(user_id)}
    🎯 Цель: {info_setting.get_what_you_want(user_id)}

    Что дальше:
    /set_role - изменить роль
    /set_what_you_want - изменить цель снова
    /close_settings - закрыть настройки
    """

        await update.message.reply_text(response_text)
        return StateType.SETTINGS
    else:
        # Если мы не ожидаем ввод и это не команда, показываем текущие настройки
        return await settings_info(update, context)