import asyncio

from pyrogram import filters

from . import *


cmd = BaseHandler(bot,"reactraid", "stopreact")

@on_message(filters.group & ~filters.me, 1)
@is_target
async def handle_incoming_messages(client: Client, message: Message):
    reaction = "🤡"
    if cmd.is_active:
        if not await react_to_message(client, message, reaction):
            LOGS.info("Failed reaction")


async def react_to_message(client, message, reaction):
    try:
        if hasattr(message, "id"):
            await asyncio.sleep(3)
            await client.send_reaction(message.chat.id, message.id, reaction)
        else:
            LOGS.info("Message not have id attribute")
            return False
    except Exception as e:
        LOGS.error(f"Error: {e}")

    return False



BotHelp("Reactionsraid").add(
    "reactraid", None, "Starts reactions raid on target user.",
).add(
    "dropreactraid", None, "Stops reactions raid on target user."
).info(
    "Reaction spammer Module"
).done()
