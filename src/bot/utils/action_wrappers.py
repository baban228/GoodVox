import asyncio
from functools import wraps
from telegram.constants import ChatAction


async def send_typing_action(update, context, func, *args, **kwargs):
    """Sends typing action while processing func command."""
    done = asyncio.Event()

    async def keep_typing():
        while not done.is_set():
            try:
                await context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id,
                    action=ChatAction.TYPING
                )
            except Exception as e:
                print(f"Error sending typing: {e}")
            try:
                await asyncio.wait_for(done.wait(), timeout=4.8)
            except asyncio.TimeoutError:
                continue

    typing_task = asyncio.create_task(keep_typing())

    # Запускаем func в отдельном потоке, если она блокирует
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, lambda: asyncio.run(func(*args, **kwargs)))
    except TypeError:
        # Если func — корутина, то делаем так:
        func_task = asyncio.create_task(func(*args, **kwargs))
        result = await func_task

    done.set()
    await typing_task

    return result


async def send_voice_record_action(update, context, func, *args, **kwargs):
    """Sends recording action while processing func command."""
    done = asyncio.Event()

    async def keep_recording():
        while not done.is_set():
            try:
                await context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id,
                    action=ChatAction.RECORD_VOICE
                )
            except Exception as e:
                print(f"Error sending voice recording: {e}")
            try:
                await asyncio.wait_for(done.wait(), timeout=4.8)
            except asyncio.TimeoutError:
                continue

    recording_task = asyncio.create_task(keep_recording())

    # Запускаем func в отдельном потоке, если она блокирует
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, lambda: asyncio.run(func(*args, **kwargs)))
    except TypeError:
        # Если func — корутина, то делаем так:
        func_task = asyncio.create_task(func(*args, **kwargs))
        result = await func_task

    done.set()
    await recording_task

    return result


async def send_upload_photo_action(update, context, func, *args, **kwargs):
    """Sends uploading photo action while processing func command."""
    done = asyncio.Event()

    async def keep_uploading_photo():
        while not done.is_set():
            try:
                await context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id,
                    action=ChatAction.UPLOAD_PHOTO
                )
            except Exception as e:
                print(f"Error sending uploading photo: {e}")
            try:
                await asyncio.wait_for(done.wait(), timeout=4.8)
            except asyncio.TimeoutError:
                continue

    uploading_photo_task = asyncio.create_task(keep_uploading_photo())

    # Запускаем func в отдельном потоке, если она блокирует
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, lambda: asyncio.run(func(*args, **kwargs)))
    except TypeError:
        # Если func — корутина, то делаем так:
        func_task = asyncio.create_task(func(*args, **kwargs))
        result = await func_task

    done.set()
    await uploading_photo_task

    return result
