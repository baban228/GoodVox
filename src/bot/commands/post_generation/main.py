from src.bot.states import *
from src.bot.utils.action_wrappers import send_upload_photo_action
from src.bot.utils.ai import AI

# req:
#   use_nko_desk: описание нко, пережеванное ии
#   cat: категория поста
#   pic_desc: описание картинки


async def post_generation_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    commands_text = f"""⚙️ {update.effective_user.first_name or 'Пользователь'}, 
    Создание поста будет происходить следующим образом:
    1) первым сообщением напиши что хотите видеть на картинке
    2) вторым сообщением напиши что хотите видеть в тексте

    Чтобы вернуться обратно:
    ❌ /skip - пропустить
    """

    await update.message.reply_text(commands_text)
    context.user_data['waiting_for'] = 'post_image_gen'
    return StateType.POST_GEN


