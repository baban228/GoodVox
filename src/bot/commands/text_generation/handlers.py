from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.commands.text_generation.InfoTextGen import InfoTextGen
from src.bot.handlers.start import start_function_command
from src.bot.states import StateType

DictInfoTextGen = dict()

async def text_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Модуль-сценарий для генерации текста"""
    try:
        keyboard = [
            ["Вернуться в главное меню"]
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Пришлите материалы (текст, фото, видео, файлы),"
                                        " которые Вы хотите использовать для генерации текста.\n"
                                        "Для начала, напишите о событии:",
                                        reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

    return StateType.TEXT_GEN

async def handle_text_generation_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if update.effective_user.id in DictInfoTextGen:
        DictInfoTextGen[update.effective_user.id].add_answer(text)
    else:
        DictInfoTextGen[update.effective_user.id] = InfoTextGen()
        DictInfoTextGen[update.effective_user.id].add_answer(text)
    await update.message.reply_text(DictInfoTextGen[update.effective_user.id].get_question())

    for i in DictInfoTextGen:
            print(f"{i}:")
            for j in DictInfoTextGen[i].get_answers():
                print(f"{j}: {DictInfoTextGen[i].get_answers()[j]}")


    if text == "Вернуться в главное меню":
        return await start_function_command(update, context)
    elif text == "Готово":
        await update.message.reply_text("Ок")

    return StateType.TEXT_GEN