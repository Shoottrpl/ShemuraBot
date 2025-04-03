import os

from aiocache import caches
from pyrogram import Client, filters
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.types import Message

from . import ShemuraBot, BotHelp, LOGS, BotHelp

cache = caches.get('default')

@ShemuraBot.bot.on_message(filters.command("clone") & ~filters.me)
async def clone(_, message: Message):
    if len(message.command) < 2:
        return await ShemuraBot.delete_message(message, "Give something correct to clone")


    text = await ShemuraBot.edit(message, "Cloning ...")

    for user in ShemuraBot.users:
        username = await user.get_users(message.command[1])

        try:
            meh = await user.resolve_peer(user.me.id)
            full_user = await user.invoke(GetFullUser(id=meh))
            about = full_user.full_user_about or ""
        except:
            about = ""

        first_name = user.me.first_name
        last_name = user.me.last_name or ""

        await cache.set(f"{user.name}_first_name", first_name)
        await cache.set(f"{user.name}_last_name", last_name)
        await cache.set(f"{user.name}_about", about)

        try:
            target_user =await user.resolve_peer(username)
            target_full_user = await user.invoke(GetFullUser(id=target_user))
            await user.update_profile(
                first_name = username.first_name,
                last_name=username.last_name or "",
                about=target_full_user.full_user.about or "",
            )
        except:
            await user.update_profile(
                first_name=username.first_name,
                last_name=username.last_name or "",
            )

        try:
            prof_pic = await user.download_media(username.photo.big_file_id)
            await user.set_profile_photo(photo=prof_pic)
            os.remove(prof_pic)
        except Exception as e:
            LOGS.error(f"Error setting profile photo {e}")

    await text.edit("Clone user success")


@ShemuraBot.bot.on_message(filters.command("revert") & ~filters.me)
async def revert(_, message: Message):
    text = await ShemuraBot.edit(message, "Reverting ...")

    for user in ShemuraBot.users:
        first_name = await cache.get(f"{user.name}_first_name")
        last_name = await cache.get(f"{user.name}_last_name")
        about = await cache.get(f"{user.name}_about")

        if not first_name:
            return await ShemuraBot.delete_message(message, "Not clone yet")

        await user.update_profile(first_name, last_name, about)

        async for photos in user.get_chat_photos("me", 1):
            await user.delete_profile_photos(photos.file_id)

        await cache.delete(f"{user.name}_first_name")
        await cache.delete(f"{user.name}_last_name")
        await cache.delete(f"{user.name}_about")


    await text.edit("Revert done")


BotHelp("Clone").add(
    "clone", None, "Clone target user account info",
).info(
    "Clone module"
).done()



