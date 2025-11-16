from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from typing import Dict, Any
from src.bot.states import *
from src.bot.utils.action_wrappers import send_typing_action
from src.bot.utils.ai import AI

# req:
#   use_nko_desk: описание нко, пережеванное ии
#   cat: категория поста
#   first_post_desc: первичное описание поста
async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt='''Ты — интеллектуальный бот-помощник для канала некоммерческой организации (НКО).
Твоя задача — генерировать посты по запросу пользователя. {use_nko_desk}''')
    promt = await send_typing_action(update, context, ai.generate_text,
        '''Ты — пользователь, который должен запромтить бота на генерацию поста категории {cat}. {use_nko_desk}
Вот официальное требование поста: {first_post_desc}''', parse_response_callback=ai.parse_qwen_wrapper_response)
    
    text = await send_typing_action(update, context, ai.generate_text,
                                    'Сгенерируй текст поста категории {cat}. Пост должен включать: {promt}',
                                    parse_response_callback=ai.parse_qwen_wrapper_response)

    await update.message.reply_text(text)

    return StateType.TEXT_GEN