import asyncio

from pyrogram import filters

from bot.functions.basic import get_client_chats, client_join_chat, get_link_chat
from . import *


@ShemuraBot.bot.on_message(filters.command("join") & ~filters.me)
async def join_chat(client: Client, message: Message):
    if message.forward_from:
        return
    try:
        chat = message.command[1]
        if chat.startswith("https://t.me/"):
            chat = chat.split("/")[-1]

    except:
        await message.reply_text("Reply or give chat name, chat id")
        return

    try:
        chat_info = await get_link_chat(client, chat)
    except Exception as e:
        await message.reply_text("Invalid chat name, pls give correct")
        LOGS.error(f"Ошибка при получении данных о чате: {e}")
        return

    text = await message.reply_text("Join chat...")
    try:
        for user in ShemuraBot.users:
            await client_join_chat(user, text, chat_info)
            LOGS.info(f"Chat info: {chat_info.username}")

        await text.edit_text(f"UserBots join chat {chat_info.username}")
    except Exception as e:
        await asyncio.sleep(10)
        await message.delete(True)
        await text.delete(True)
        LOGS.error(f"Ошибка при вступлении в чат: {e}")
        return

BotHelp("Joinchat").add(
    "join", None,"Join to linked chat of public channel or group", "join @somechatname"
).info(
    "Join chat to iteract plugin"
).done()

