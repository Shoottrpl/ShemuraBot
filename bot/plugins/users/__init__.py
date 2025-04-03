from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Message

from bot.core.clients import ShemuraBot
from bot.core.config import Config, Symbols
from bot.plugins.help import BotHelp
from bot.plugins.basehandler import BaseHandler
from bot.plugins.decorator import on_message
from bot.core.logger import LOGS


bot = ShemuraBot.bot

bot_only = [ChatType.BOT]
group_only = [ChatType.GROUP, ChatType.SUPERGROUP]
group_channel = [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]
private_bot = [ChatType.PRIVATE, ChatType.BOT]
private_only = [ChatType.PRIVATE]


que = []

def is_target(func):
    async def get_u(client: Client, message: Message):
        if not message.from_user:
            return

        username = f"@{message.from_user.username}"

        if username not in que:
            return
        else:
            return await func(client, message)

    return get_u





