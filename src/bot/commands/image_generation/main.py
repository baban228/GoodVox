from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from typing import Dict, Any

from src.bot.commands.info_of_nko.Info_of_nko import info_storage
from src.bot.commands.settings.Info_settings import info_setting
from src.bot.states import *
from src.bot.utils.action_wrappers import send_upload_photo_action
from src.bot.utils.ai import AI

# req:
#   use_nko_desk: описание нко, пережеванное ии
#   cat: категория поста
#   pic_desc: описание картинки


async def image_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
    Напишите, что вы хотите видеть на картинке

    Чтобы вернуться обратно:
    ❌ /skip - пропустить
    """

    await update.message.reply_text(commands_text)

    return StateType.IMAGE_GEN


async def generation_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pic_desc = update.message.text.strip()
    user_id = update.effective_user.id
    use_nko_desk = info_storage.get_info_as_string(user_id)
    role_ai = info_setting.get_role(user_id)
    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt=f"""Ты — {role_ai} для канала некоммерческой организации (НКО).
Твоя задача — генерировать посты по запросу пользователя. {use_nko_desk}""")

    text = await send_upload_photo_action(update, context, ai.generate_image,
                                          f"""Сгенерируй изображение для поста НКО. {use_nko_desk} {pic_desc}""",
                                          parse_response_callback=ai.parse_qwen_wrapper_response)
    await update.message.reply_text(text)

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
        если хотите новую картинку просто напиши ниже текст

        Чтобы вернуться на главное меню:
        ❌ /skip - вернуться
        """

    await update.message.reply_text(commands_text)
    return StateType.IMAGE_GEN