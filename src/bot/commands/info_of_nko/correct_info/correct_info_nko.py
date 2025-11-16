from telegram import Update
from telegram.ext import ContextTypes
from src.bot.states import StateType

from src.bot.commands.info_of_nko.Info_of_nko import info_storage


async def show_current_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    # Получаем текущую информацию
    current_info = info_storage.get_info(user_id)

    # Формируем текст с текущей информацией
    if current_info:
        info_list_str = ""
        for i, item in enumerate(current_info, 1):
            info_list_str += item
        # Убираем последний перенос строки
        info_list_str = info_list_str.rstrip('\n')
    else:
        info_list_str = "Пока нет информации."

    commands_text = f"""👤 {update.effective_user.first_name or 'Пользователь'}, 
вот что у вас сейчас есть:

{info_list_str}

➕ Чтобы добавить еще информациюпросто пишите ниже
🗑️ Чтобы написать все сначала, нажмите /remove_all_nko
👀 Чтобы посмотреть что сейчас написано, нажмите /get_nko
⏪ Чтобы удалить последнюю запись, нажмите /remove_last_nko
❌ Чтобы отменить — нажмите /skip
"""

    await update.message.reply_text(commands_text)

    return StateType.COLL_INFO


async def remove_all_nko(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    info_storage.clear_info(user_id)
    commands_text = f"""🗑️ {update.effective_user.first_name or 'Пользователь'}, вся информация успешно стерта! 

➕ Можете начать заново — просто напишите что-нибудь ниже"""
    await update.message.reply_text(commands_text)

    return StateType.COLL_INFO


async def remove_last_nko(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    removed_item = info_storage.remove_last_entry(user_id)

    if removed_item:
        commands_text = f"""⏪ {update.effective_user.first_name or 'Пользователь'}, последняя запись успешно удалена:

❌ "{removed_item}"

➕ Продолжайте вводить информацию ниже"""
    else:
        commands_text = f"""⚠️ {update.effective_user.first_name or 'Пользователь'}, нет записей для удаления.

➕ Начните вводить информацию с чистого листа"""

    await update.message.reply_text(commands_text)

    return StateType.COLL_INFO