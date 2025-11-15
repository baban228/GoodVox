from telegram import Update
from telegram.ext import ContextTypes

from src.bot.states import StateType, set_user_state, StateMachine


async def start_function_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """может понадобится"""
    #telegram_user_id = update.effective_user.id
    #username = update.effective_user.username or f'user_{telegram_user_id}'
    #first_name = update.effective_user.first_name or 'Unknown User'


    welcome_text = f"""🌟 Привет, {update.effective_user.first_name or 'Пользователь'}!

Я — бот, помогающий генерировать контент для НКО. 
Для начала, заполните информацию об организации. 
Можно присылать текст, картинки и видео одним сообщением. 
Не волнуйтесь, информацию об организации можно будет изменить в любое время.

❌ /skip - пропустить заполнение
"""

    await update.message.reply_text(welcome_text)

    return StateType.COLL_INFO

#тут еще надо реализовать отправку данных на бд
async def skip_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    commands_text = f"""👋 Привет, {update.effective_user.first_name or 'Пользователь'}!

✨ Доступные команды:

📝 /text_generation - генерация текста
🖼️ /image_generator - генерация картинок
✏️ /correct_text - редактирование текста
📅 /plan - создание плана
🏢 /correct_info_nko - редактировать информацию об НКО
⚙️ /settings - настройки нейронки
"""

    await update.message.reply_text(commands_text)
    return StateType.MAIN_MENU