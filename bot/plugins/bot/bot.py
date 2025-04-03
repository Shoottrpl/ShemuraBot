from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, Message

from bot.core import LOGS
from bot.functions.tools import restart

from ..Generalbuttons import gen_bot_help_buttons, start_button
from . import HELP_MESSAGE, START_MSG, BotHelp, ShemuraBot
from ... import Config


@ShemuraBot.bot.on_message(filters.command("start"))
async def start(_, message: Message):
    btns = start_button()

    await message.reply_text(
        START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(btns)
    )

@ShemuraBot.bot.on_message(filters.command("help"))
async def help_pm(_, message: Message):
    btns = await gen_bot_help_buttons()

    await message.reply_text(
        HELP_MESSAGE,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(btns),
    )


@ShemuraBot.bot.on_message(filters.command("restart"))
async def restart_client(_, message: Message):
    await message.reply_text("Restart complete")
    try:
        await restart()
    except Exception as e:
        LOGS.error(e)

(BotHelp("Bot").add(
     "start", None,"Command to start bot and get botmenu"
 ).add(
     "help", None, "Get help menu with all command for assist bot"
 ).add(
     "restart", None, "Restart the bot"
 ).info(
     "Base command of this bot"
 ).done())