import asyncio

from pyrogram import idle
from bot.core import ShemuraBot, UserSetup, Config
from bot.functions.tools import init_git


async def main():
    await ShemuraBot.activate()
    await UserSetup()
    # await init_git(Config.GIT_REP)
    await idle()


if __name__ == "__main__":
    ShemuraBot.run(main())

