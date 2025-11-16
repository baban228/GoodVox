from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from src.bot.states import *
from src.bot.utils.action_wrappers import send_upload_photo_action
from src.bot.utils.ai import AI

from .Info_post_gen import info_post_gen
from src.bot.commands.info_of_nko.Info_of_nko import info_storage
from src.bot.commands.settings.Info_settings import info_setting

from src.bot.handlers.start import skip_function

async def generation_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user_id = update.effective_user.id
    post_image_text = info_post_gen.get_image(user_id)
    post_text_text = info_post_gen.get_text(user_id)
    role_ai = info_setting.get_role(user_id)
    use_nko_desk = info_storage.get_info_as_string(user_id)


    #ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
     #       system_prompt=f"""Ты — {role_ai} для канала некоммерческой организации (НКО).
#Твоя задача — генерировать посты по запросу пользователя. {use_nko_desk}""")

    #text = await send_upload_photo_action(update, context, ai.generate_image,
     #                                     f"""Сгенерируй изображение для поста НКО. {use_nko_desk} {post_image_text}""",
     #                                     parse_response_callback=ai.parse_qwen_wrapper_response)
   # await update.message.reply_text(text)

   # text = await send_upload_photo_action(update, context, ai.generate_image,
    #                                      f"""Сгенерируй текст для поста НКО. {use_nko_desk} {post_text_text}""",
    #                                      parse_response_callback=ai.parse_qwen_wrapper_response)
    #await update.message.reply_text(text)

    print(post_image_text, " ", post_text_text, " ", role_ai, " ", use_nko_desk)
    return await skip_function(update, context)