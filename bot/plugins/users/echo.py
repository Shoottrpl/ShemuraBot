import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait

from . import *

cmd = BaseHandler(bot,"echo", "unecho")

@on_message(filters.incoming & ~filters.group & ~filters.service & ~filters.me)
@is_target
async def echo_handler(_, message: Message):
    if cmd.is_active:
        try:
            if message.sticker:
                await message.reply_sticker(message.sticker.file_id)
            else:
                await message.reply(message.text)
        except FloodWait as e:
            await asyncio.sleep(e.value)

BotHelp("Echo").add(
    "echo", None, "Start echo message on target user",
).add(
    "unecho", None, "Stop echo message on target user",
).info(
    "Echo module"
).done()
