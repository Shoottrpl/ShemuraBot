import asyncio
from cgitb import handler

from pyrogram import Client, enums
from pyrogram.types import Message, User
from bot.core.logger import LOGS


async def get_link_chat(client: Client, chat_id: int):
    try:
        chat_details = await client.get_chat(chat_id)
    except Exception as e:
        LOGS.error(f"{e}")
    if getattr(chat_details, 'linked_chat', None):
        link_chat = chat_details.linked_chat

        return link_chat

async def get_client_chats(client: Client,
                           chat_type: list =
                           [enums.ChatType.CHANNEL,
                            enums.ChatType.SUPERGROUP,]
):
    ub_chats = []

    async for dialog in client.get_dialogs():
        if dialog.chat.type in chat_type and dialog.chat.id not in ub_chats:
            ub_chats.append(dialog.chat.id)

    return ub_chats


async def client_join_chat(client: Client, text, chat):
        chats = await get_client_chats(client)

        if chat.id in chats:
            await text.edit_text(f"{client.name} is already in chat {chat.username}")
            return

        try:
            await asyncio.sleep(3)
            await client.join_chat(chat.username)
        except Exception as e:
            if 'INVITE_REQUEST_SENT' in str(e):
                LOGS.info(f"{client.name} sent join request to {chat.username}, waiting for processing.")
            else:
                LOGS.error(f"Error joining chat: {e}")


def GetFromUserID(message: Message):
    return message.from_user.id

def GetChatID(message: Message):
    return message.chat.id

def GetUserMention(user: User):
    if user.username:
        username = f"@{user.username}"
    else:
        if user.last_name:
            name = f"{user.first_name} {user.last_name}"
        else:
            name = f"{user.first_name}"

    username = f"<a href='tg://user?id={user.id}'>{name}</a>"

    return username






