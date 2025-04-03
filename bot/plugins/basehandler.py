import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from bot.core.logger import LOGS

class BaseHandler:
    def __init__(self, client: Client, activate_command: str, deactivate_command: str):
        self.client = client
        self.activate_command = activate_command.split()[0]
        self.deactivate_command = deactivate_command
        self.is_active = False
        self.register_handler()

    def register_handler(self):
        @self.client.on_message(filters.command(self.activate_command) & ~filters.me)
        async def start_handler(client: Client, message: Message):
            await self.activate()
            await message.reply_text(f"{self.activate_command} activate")

        @self.client.on_message(filters.command(self.deactivate_command) & ~filters.me)
        async def stop_handler(client: Client, message: Message):
            await self.deactivate()
            await message.reply_text(f"{self.activate_command} deactivate")

    async def activate(self):
        self.is_active = True
        LOGS.info(f"message hand {self.is_active}")

    async def deactivate(self):
        self.is_active = False
        LOGS.info(f"message unhand {self.is_active}")

