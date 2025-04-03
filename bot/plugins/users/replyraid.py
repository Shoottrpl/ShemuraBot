import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatAction

from . import *


cmd = BaseHandler(bot,"replyraid", "dropraid")

@on_message(filters.group & ~filters.me, 2)
@is_target
async def reply_raid(client: Client, message: Message):
    if cmd.is_active:
        LOGS.info(f"{message.chat.id} received a message")
        text = "-" # all you want
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(10)
            await message.reply_text(text)
            await client.send_chat_action(message.chat.id, ChatAction.CANCEL)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            LOGS.info(f"{e}")

BotHelp("Replyraid").add(
    "replyraid", None, "Starts reply raid on target user.",
).add(
    "dropreplyraid", None, "Stops reply raid on target user."
).info(
    "Spammer Module"
).done()























