from telegram import Update
from telegram.ext import ContextTypes

from src.bot.states import StateType
from src.bot.commands.text_generation.text_generation_main import text_generation_main

async def handle_text_command_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    command = update.message.text.split()[0]
    '''Тут создаются новые команды'''
    if command == "/text_generation":
        return await text_generation_main(update, context)
    elif command == "/image_generator":
        return await text_generation_main(update, context) #это заглушка
    elif command == "/correct_text":
        return await text_generation_main(update, context) #это заглушка
    elif command == "/plan":
        return await text_generation_main(update, context) #это заглушка
    else:
        return StateType.MAIN_MENU