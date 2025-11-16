from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from typing import Dict, Any

from src.bot.commands.info_of_nko.Info_of_nko import info_storage
from src.bot.states import *
from src.bot.utils.action_wrappers import send_upload_photo_action
from src.bot.utils.ai import AI
from src.bot.commands.settings.Info_settings import info_setting
# req:
#   use_nko_desk: описание нко, пережеванное ии
#   cat: категория поста
#   pic_desc: описание картинки


async def correct_text_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
    Напишите, что вы хотите исправить в тексте

    Чтобы вернуться обратно:
    ❌ /skip - пропустить
    """

    await update.message.reply_text(commands_text)

    return StateType.COR_TEXT


async def regeneration_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text_correct_desc = update.message.text.strip()
    user_id = update.effective_user.id
    role_ai = info_setting.get_role(user_id)


    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt=f"""Ты — {role_ai}.
Твоя задача — проверить текст на орфографические ошибки по запросу пользователя.""")

    print(f"""Проверить текст на орфографические ошибки: {text_correct_desc}""")

    '''Тут сделай запрос на нейронку, '''
    #text = await send_upload_photo_action(update, context, ai.generate_image,
    #                                      f"""Сгенерируй изображение для поста НКО. {use_nko_desk} {pic_desc}""",
    #                                      parse_response_callback=ai.parse_qwen_wrapper_response)
    #await update.message.reply_text(text)

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
        если хотите исправить новый текст, просто пишите его ниже

        Чтобы вернуться на главное меню:
        ❌ /skip - вернуться
        """

    await update.message.reply_text(commands_text)
    return StateType.COR_TEXT