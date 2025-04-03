import asyncio

from pyrogram import Client
from bot.core import ShemuraBot, LOGS

Task = {}

async def spam_text(
        chat_id: str,
        to_spam: str,
        count: int,
        reply_to: int,
        delay: float,
        copy_id: int,
        event: asyncio.Event,
):
    clients = ShemuraBot.users

    for _ in range(count):
        if event.is_set():
            break
        for client in clients:
            if copy_id:
                await client.copy_message(
                    chat_id, chat_id, copy_id, reply_to_message_id=reply_to
                )
            else:
                await client.send_message(
                    chat_id,
                    to_spam,
                    disable_web_page_preview=True,
                    reply_to_message_id=reply_to,
                )

            if delay:
                await asyncio.sleep(delay)

    try:
        event.set()
        task = Task.get(chat_id, None)
        if task:
            task.remove(event)
    except Exception as e:
        LOGS.error(f"{e}")

