from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from typing import Dict, Any
from src.bot.states import *
from src.bot.utils.action_wrappers import send_upload_photo_action
from src.bot.utils.ai import AI

# req:
#   use_nko_desk: описание нко, пережеванное ии
#   cat: категория поста
#   pic_desc: описание картинки
async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt='''Ты — интеллектуальный бот-помощник для канала некоммерческой организации (НКО).
Твоя задача — генерировать посты по запросу пользователя. {use_nko_desk}''')
    
    text = await send_upload_photo_action(update, context, ai.generate_image,
                                    'Сгенерируй изображение для поста НКО. {use_nko_desk} {pic_desc}',
                                    parse_response_callback=ai.parse_qwen_wrapper_response)

    await update.message.reply_text(text)

    return StateType.TEXT_GEN