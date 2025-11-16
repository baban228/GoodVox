from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.commands.text_generation.InfoTextGen import InfoTextGen
from src.bot.handlers.start import start_function_command
from src.bot.states import StateType
from src.bot.utils.action_wrappers import send_typing_action
from src.bot.utils.ai import AI
from src.bot.commands.info_of_nko import info_storage

DictInfoTextGen = dict()

async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Модуль-сценарий для генерации текста"""
    try:
        keyboard = [
            ["Вернуться в главное меню"]
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Укажите категорию поста",
                                        reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

    return StateType.TEXT_GEN

async def handle_text_generation_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id

    # making session with values
    if user_id not in DictInfoTextGen:
        DictInfoTextGen[user_id] = InfoTextGen()
    session = DictInfoTextGen[user_id]

    if text == "Вернуться в главное меню":
        return await start_function_command(update, context)

    # saving answer
    if session.current_question:
        session.add_answer(session.current_question, text)

    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions')

    # 1) check for data sufficiency
    analysis_prompt = f"""
Ты — эксперт по созданию постов для НКО.

Вот категория поста: {session.get_cat()}
Вот ранее собранные данные:
{session.get_answers_as_text()}

Определи, достаточно ли данных для генерации качественного поста.

Ответь строго в JSON:
Если достаточно:
    {{"enough": true}}
Если недостаточно:
    {{"enough": false, "question": "следующий вопрос пользователю"}}
"""

    analysis_raw = await send_typing_action(
        update, context, ai.generate_text,
        analysis_prompt,
        parse_response_callback=ai.parse_qwen_wrapper_response
    )

    # json parse
    import json
    try:
        analysis = json.loads(analysis_raw)
    except:
        analysis = {"enough": False, "question": "Можешь уточнить детали?"}

    # 2) creating new question if data insufficiency
    if not analysis.get("enough"):
        next_q = analysis.get("question", "Уточни, пожалуйста?")
        session.current_question = next_q

        await update.message.reply_text(next_q)
        return StateType.TEXT_GEN

    # 3) creating post if data sufficiency
    final_prompt = f"""
Создай пост категории {session.get_cat()}.

Данные, полученные от пользователя:
{session.get_answers_as_text()}

Сформируй развернутый текст поста.
"""

    final_text = await send_typing_action(
        update, context, ai.generate_text,
        final_prompt,
        system_promt="""Ты — интеллектуальный помощник НКО. Твоя задача — писать достойные, аккуратные, точные посты.""",
        parse_response_callback=ai.parse_qwen_wrapper_response
    )

    await update.message.reply_text(final_text)

    session.reset()

    return StateType.TEXT_GEN

