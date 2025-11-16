from src.bot.states import *
from src.bot.commands.post_generation.main import *

from .Info_post_gen import info_post_gen
from .ai_generation import generation_post


async def handle_post_messages(update, context):
    user_message = update.message.text.strip()
    user_id = update.effective_user.id

    # Проверяем, не ожидаем ли мы ввод
    user_state = context.user_data.get('waiting_for')

    if user_state == 'post_image_gen':
        # Обрабатываем ввод новой роли
        gen_post_image = user_message
        info_post_gen.add_image(user_id, gen_post_image)
        context.user_data['waiting_for'] = None  # Сбрасываем состояние

        response_text = f"""Информация принята! Далее опишем текст
    
    Чтобы вернуться на главное меню:
    ❌ /skip - вернуться
    """

        await update.message.reply_text(response_text)
        context.user_data['waiting_for'] = 'post_text_gen'
        return StateType.POST_GEN

    elif user_state == 'post_text_gen':
        # Обрабатываем ввод новой цели
        gen_post_text = user_message
        info_post_gen.add_text(user_id, gen_post_text)
        context.user_data['waiting_for'] = None  # Сбрасываем состояние

        response_text = f"""Информация принята! ожидайте
    
    Чтобы вернуться на главное меню:
    ❌ /skip - вернуться
    """

        await update.message.reply_text(response_text)
        return await generation_post(update, context)
    else:
        # Если мы не ожидаем ввод и это не команда, показываем текущие настройки
        return await post_generation_main(update, context)

