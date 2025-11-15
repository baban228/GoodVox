from telegram import Update
from telegram.ext import ContextTypes
from src.bot.states import StateType


async def collection_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text.strip()

    if 'collected_info' not in context.user_data:
        context.user_data['collected_info'] = []

    context.user_data['collected_info'].append(user_text)

    print(f"Сохранённый ввод: {context.user_data['collected_info']}")

    commands_text = f"""{update.effective_user.first_name or 'Пользователь'}, спасибо! 
Информация сохранена.
Можете прислать ещё или пропустить этот шаг и перейти дальше
/skip - пропустить
"""

    await update.message.reply_text(commands_text)

    return StateType.COLL_INFO