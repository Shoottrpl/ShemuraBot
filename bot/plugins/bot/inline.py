from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineQuery, InlineQueryResult, InputTextMessageContent, \
    InlineQueryResultArticle, Message

from . import Config, ShemuraBot, LOGS



@ShemuraBot.bot.on_inline_query()
async def help_inline(_, query: InlineQuery):
    LOGS.info(f"Received query: {query}")
    inline_query = query.query.lower()
    LOGS.info(f"Received inline query: {inline_query}")

    if not inline_query:
        LOGS.info("Empty inline query, returning...")
        return

    result = [
        InlineQueryResultArticle(
            command,
            input_message_content=InputTextMessageContent(f"/{command}"),
            description=Config.BOT_CMD_INFO.get(command, "Description does exist")["description"]
        )
        for command in Config.BOT_CMD_INFO  if command.startswith(inline_query)
    ]

    LOGS.info(f"Inline query results: {result}")
    try:
        await ShemuraBot.bot.answer_inline_query(query.id, result)
    except Exception as e:
        LOGS.error(f"Error answering inline query: {e}")
    

@ShemuraBot.bot.on_message(filters.me)
async def set_commands(_, message: Message):
    commands = [(command, command.get("description", "Description does exist")) for command in Config.BOT_CMD_INFO]
    await ShemuraBot.set_bot_commands(commands)



