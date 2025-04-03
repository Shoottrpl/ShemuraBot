import asyncio
import functools
import glob
import os
import importlib.util
import sys
import time
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, BotCommand
from bot.sessions.get_session import get_sessions

from .logger import LOGS
from .config import Symbols, Config





loop = asyncio.get_event_loop()

class ShemuraClient(Client):
    def __init__(self) -> None:
        self.users: list[Client] = []
        self.listening = {}
        self.bot: Client = Client(
            name="SheMura 1.0",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="Bot.plugins.bot"),
            workdir=Config.WORKDIR,
        )
        self.bot.add_handler(MessageHandler(self.use_listner))

    async def start_users(self) -> None:
        sessions = get_sessions()
        tasks = []
        for i, session_str in enumerate(sessions):
            tasks.append(self.start_client(i, session_str))
        await asyncio.gather(*tasks)


    async def start_client(self, i, session_str):
        try:
            app = Client(
                name=f"UserBot{i + 1}",
                session_string=session_str,
                # api_id=session["api_id"],
                # api_hash=session["api_hash"],
                # phone_number=session["phone_number"],
                # password=session["password"],
                workdir=Config.WORKDIR,
            )
            await app.start()
            self.users.append(app)
        except Exception as e:
            LOGS.error(f"{i + 1}: {e}")


    async def start_bot(self):
        await self.bot.start()
        me = await self.bot.get_me()
        LOGS.info(f"Start ShemuraBot Client: '{me.username}'")

    async def load_plugins(self) -> None:
        count = 0
        files = glob.glob("./bot/plugins/users/*.py")

        for file in files:
            path = Path(file)
            shortname = path.stem.replace(".py", "")
            if shortname.startswith("__"):
                continue
            try:
                name = "bot.plugins.users." + shortname
                spec = importlib.util.spec_from_file_location(name, file)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules[name] = load

                LOGS.info(f"Loaded plugin: {shortname}")
                count += 1

            except Exception as e:
                LOGS.error(f"Failed to load plugin {shortname}: {e}")

        LOGS.info(f"Loader Plugins {count}")



    async def validate_logger(self, client: Client) -> bool:
        try:
            await client.get_chat_member(Config.LOGGER_ID, "me")
            return True
        except Exception:
            return await self.join_logger(client)

    async def join_logger(self, client: Client):
        try:
            invite_link = await self.bot.export_chat_invite_link(Config.LOGGER_ID)
            await client.join_chat(invite_link)
            return True
        except Exception:
            return False

    async def set_commands(self) -> None:
        commands = [
            BotCommand(command, Config.BOT_CMD_INFO[command].get('description', 'Description does exist'))
            for command in Config.BOT_CMD_INFO
        ]
        await self.bot.set_bot_commands(commands)

    async def activate(self) -> None:
        LOGS.info(
            f"{Symbols.bullet * 3} Start UserBot Clients {Symbols.bullet * 3}"
        )
        start_time = time.time()
        await self.start_bot()
        await self.start_users()
        await self.load_plugins()
        await self.set_commands()
        duration = time.time() - start_time
        LOGS.info(f"Start time: {duration:.2f} секунд")


class CustomMethods(ShemuraClient):
    async def get_input(self, message: Message) -> str:
        if len(message.command) < 2:
            output = ""
        else:
            try:
                output = message.text.split(" ")
            except IndexError:
                output = ""

        return output

    async def get_dialogs(self):
        try:
            async for dialog in self.get_dialogs():
                LOGS.info(f"Dialog: {dialog.chat.title}")
        except Exception as e:
            LOGS.error(f"Error: {e}")

    async def edit(
            self,
            message: Message,
            text: str,
            parse_mode: ParseMode = ParseMode.DEFAULT,
            no_link_preview: bool = True,
    ) -> Message:
        if message.from_user:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(
                    text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=no_link_preview,
                )
            return await message.reply_text(
                text,
                parse_mode=parse_mode,
                disable_web_page_preview=no_link_preview,
            )
        return await message.edit_text(
            text,
            parse_mode=parse_mode,
            disable_web_page_preview=no_link_preview,
        )

    async def _delete(self, message: Message, delay: int = 0) -> None:
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except Exception as e:
            LOGS.info(f"{e} {message}")

    async def delete_message(self, message: Message, text: str, delete: int = 10, in_background: bool = True) -> None:
        to_del = await self.edit(message, text)
        if in_background:
            asyncio.create_task(self._delete(to_del, delete))
        else:
            await self._delete(to_del, delete)


    async def ask(self, chat_id: int, text: str, timeout: int, *args, **kwargs):
        await self.bot.send_message(chat_id, text, *args, **kwargs)
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        future.add_done_callback(functools.partial(lambda _, uid: self.listening.pop(uid, None), chat_id))

        self.listening[chat_id] = {"task": future}

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            await self.bot.send_message(chat_id, f"Not answered for {timeout} seconds")
            self.listening.pop(chat_id, None)
            return None

    async def use_listner(self, _, msg: Message):
        lstn = self.listening.get(msg.chat.id)
        if lstn and not lstn["task"].done():
            lstn["task"].set_result(msg)
        return msg.continue_propagation()



ShemuraBot = CustomMethods()





