from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from typing import Dict, Any
from src.bot.states import *
from src.bot.utils.action_wrappers import send_typing_action
from src.bot.utils.ai import AI


def parse_raw_response(response: Dict[str, Any]):
    import json

    # извлечь текст ответа
    try:
        choices = response.get("choices") or []
        if choices:
            msg = choices[0].get("message") or choices[0]
            content = msg.get("content")
            # если content — list rich parts
            if isinstance(content, list):
                text_out = " ".join((p.get("text") or p.get("content") or "") for p in content if isinstance(p, dict))
            else:
                text_out = content if isinstance(content, str) else str(content)
        else:
            # fallback
            text_out = response.get("message") or response.get("result") or response.get("text") or json.dumps(response, ensure_ascii=False)
    except Exception:
        text_out = json.dumps(response, ensure_ascii=False)
    return text_out


async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt='''Ты — интеллектуальный бот-помощник для канала некоммерческой организации (НКО).
Твоя задача — генерировать посты по запросу пользователя. {use_nko_desk}''')
    text = await send_typing_action(update, context, ai.generate_text,
        '''Ты — пользователь, который должен запромтить бота на генерацию поста категории {cat}. {use_nko_desk}
Вот официальное требование поста: {first_post_desc}''', parse_response_callback=parse_raw_response)

    await update.message.reply_text(text)

    return StateType.TEXT_GEN