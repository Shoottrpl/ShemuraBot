from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from bot.core import ShemuraBot

def on_message(filters: filters.Filter, group: int = 0):
    def decorator(func):
        async def wrapper(client: Client, message: Message):
            await func(client, message)
            message.continue_propagation()

        for user in ShemuraBot.users:
            user.add_handler(MessageHandler(wrapper, filters), group)

        return wrapper

    return decorator