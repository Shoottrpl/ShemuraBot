import asyncio

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, MessageDeleteForbidden
from pyrogram.types import Message

from . import ShemuraBot, LOGS


def _chunk(from_msg: int):
    curr_msg = from_msg
    to_msg = from_msg - 100

    while curr_msg > 0:
        yield list(range(to_msg, curr_msg))
        curr_msg = to_msg
        to_msg -= 100

@ShemuraBot.bot.on_message(filters.command("purge") & ~filters.me)
async def purge_message(client: Client, message: Message):
    if not message.reply_to_message:
        return await ShemuraBot.delete_message(
            message, "Reply to delete all messages after that"
        )

    delete = 0
    from_msg = message.reply_to_message

    text = await ShemuraBot.edit(message, "Purging ...")
    count = 0

    for i in _chunk(from_msg.id+1):
        LOGS.info(f"{i}")
        try:
            count += 1
            await ShemuraBot.bot.delete_messages(
                chat_id=message.chat.id, message_ids=i, revoke=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except MessageDeleteForbidden as e:
            LOGS.warning(f"cannot delete message - permision denied")
        except Exception as e:
            LOGS.error(f"Error: {e} {i}")

    LOGS.info(f"{from_msg}")
    done = await text.edit(f"Purging done. Success delete messages {count}")
    await asyncio.sleep(2)
    await done.delete()


