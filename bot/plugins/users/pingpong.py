import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatAction

from . import *

cmd = BaseHandler(bot,"pingpong", "stop")

@on_message(filters.group & ~filters.me, 1)
async def ping_pong(_, message: Message):
    text_to_reply = "+"

    if cmd.is_active:
        clients = ShemuraBot.users

        for client in ShemuraBot.users:
            me = await client.get_me()

            if message.text == "+":
                try:
                    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                    await asyncio.sleep(10)
                    await message.reply_text(text_to_reply)
                    await client.send_chat_action(message.chat.id, ChatAction.CANCEL)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    LOGS.info(f"{e}")
