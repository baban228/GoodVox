from telegram import Update
from telegram.ext import ContextTypes
from src.bot.states import StateType

from src.bot.commands.info_of_nko.Info_of_nko import info_storage


async def collection_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text.strip()
    user_id = update.effective_user.id

    # Добавляем информацию в хранилище
    info_storage.add_info(user_id, user_text)

    commands_text = f"""✅ {update.effective_user.first_name or 'Пользователь'}, информация успешно сохранена! 

✨ Доступные команды:

➕ Можете прислать ещё информацию
❌ /skip - пропустить и перейти дальше
📋 /get_nko - посмотреть что уже добавлено

📝 /text_generation - создание текста
🖼️ /image_generator - создание картинок
🖼️ /post_generation - создание поста
✏️ /correct_text - редактирование текста
📅 /plan - создание плана
🏢 /correct_info_nko - редактировать информацию об НКО
⚙️ /settings - настройки нейронки
"""

    await update.message.reply_text(commands_text)

    return StateType.COLL_INFO