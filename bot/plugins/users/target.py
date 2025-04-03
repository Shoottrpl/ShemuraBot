import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from . import ShemuraBot, BotHelp, que, LOGS



@ShemuraBot.bot.on_message(filters.command("target") & ~filters.me)
async def activate_reply_flood(client: Client, message: Message):
    if message.forward_from:
        return

    if message.reply_to_message_id:
        reply_to = message.reply_to_message.from_user
        user_id = reply_to.id
        username = f"@{reply_to.username}" if reply_to.username else reply_to.mention
        text = await message.reply_text("Target initialing....")
        if not reply_to:
            await message.reply_text("Reply to user")
            return
        if user_id not in que:
            que.append(user_id)
            await text.edit_text(f"Target {username}")
        else:
            await text.edit_text(f"Target already exist")
    else:
        try:
            user = int(message.command[1])
        except ValueError:
            user = message.command[1]
        except:
            await message.reply_text("Reply or give username, peer id")
            return
        try:
            user = await client.get_users(user)
        except Exception:
            text = await message.reply_text("The user does not exist")
            await asyncio.sleep(10)
            await message.delete(True)
            await text.delete(True)
            return

        text = await message.reply_text("Target initialing...")
        username = f"@{user.username}" if user.username else user.mention

        if username not in que:
            que.append(username)
            await text.edit_text(f"Target {username}")
        else:
            await text.edit_text(f"Target already exist")


@ShemuraBot.bot.on_message(filters.command("droptarget") & ~filters.me)
async def deactivate_reply_flood(client: Client, message: Message):
    if message.forward_from:
        return

    if message.reply_to_message_id:
        reply_to = message.reply_to_message.from_user
        if not reply_to:
            await message.reply_text("Reply to user")
            return
        user_id = reply_to.id
        username = f"@{reply_to.username}" if reply_to.username else reply_to.mention
        text = await message.reply_text("Target dropping...")
        try:
            if user_id in que:
                que.remove(user_id)
                await text.edit_text(f"Drop target: {username} ")
                return
        except Exception:
            await text.edit_text("Target not exist")
            return
    else:
        try:
            user = int(message.command[1])
        except ValueError:
            user = message.command[1]
        except:
            await message.reply_text("Reply or give username, peer id")
            return
        try:
            user = await client.get_users(user)
            LOGS.info(f"{user}")
        except Exception:
            text = await message.reply_text("The user does not exist")
            await asyncio.sleep(10)
            await message.delete(True)
            await text.delete(True)
            return
        text = await message.reply_text("Target dropping..")
        user_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        try:
            if user_id in que:
                que.remove(user_id)
                await text.edit_text(f"Drop target: {username}")
                return
        except Exception:
            await text.edit_text("Target not exist")
            return


BotHelp("Target").add(
    "target", None, "Initial target to interact",
).add(
    "droptarget", None, "Drop target"
).info(
    "Targeting plugin"
).done()
