import asyncio

from pyrogram import filters
from pyrogram.types import Message

from bot.functions.spam_text import spam_text, Task
from . import ShemuraBot, BotHelp, que


@ShemuraBot.bot.on_message(filters.command("spam") & ~filters.me)
async def spam_message(_, message: Message):
    if len(message.command) < 4:
        return await ShemuraBot.delete_message(message, "Give something correct to spam")

    chats = [*que]
    reply_to = message.reply_to_message.id if message.reply_to_message else None

    try:
        count = int(message.command[1])
    except ValueError:
        return await ShemuraBot.bot.delete_messages(message, "Give number of spam")

    try:
        delay = int(message.command[2])
    except ValueError:
        return await ShemuraBot.bot.delete_messages(message, "Give number of delay")

    to_spam = message.text.split(" ", 3)[3].strip()

    for chat_name in chats:
        event = asyncio.Event()
        task = asyncio.create_task(
            spam_text(chat_name, to_spam, count, reply_to, delay, None, event)
        )

        if Task.get(chat_name, None):
                Task[chat_name].append(event)
        else:
            Task[chat_name] = [event]

    await message.delete()
    await task


@ShemuraBot.bot.on_message(filters.command("stopspam") & ~filters.me)
async def stop_spam(_, message: Message):
    chat_name = message.command[1]

    if not Task.get(chat_name, None):
        return await ShemuraBot.delete_message(message, "No currently spam task for this chat")

    for event in Task[chat_name]:
        event.set()

    del Task[chat_name]
    await ShemuraBot.delete_message(message, f"Spam task stopped for {chat_name}")


@ShemuraBot.bot.on_message(filters.command("listspam") & ~filters.me)
async def list_spam(_, message: Message):
    active_spams = list(Task.keys())

    text = "Active spam Tasks"
    for active in active_spams:
        text += f"{active} \n"

    await ShemuraBot.edit(message, text)


BotHelp("Spam").add(
    "spam",
    "<count><delay><message>",
    "Spam message in chat target users count times with delay",
    "spam 10 4 hello",
    "Be careful spams userbots go ban"
).add(
    "stopspam",
    None,
    "Stop spam task on target",
    "stopspam @user",
).add(
    "listspam",
    None,
    "List all currently spam task",
    "listspam",
).info(
    "Spam messages"
).done()



