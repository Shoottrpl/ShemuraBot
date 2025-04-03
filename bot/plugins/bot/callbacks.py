from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.filters import caption
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..Generalbuttons import gen_bot_help_buttons, start_button
from . import HELP_MESSAGE, START_MSG, Config, ShemuraBot, LOGS




@ShemuraBot.bot.on_callback_query(filters.regex(r"close"))
async def close(_, cb: CallbackQuery):
    await cb.message.delete()


@ShemuraBot.bot.on_callback_query(filters.regex(r"bot_help_menu"))
async def bot_help_menu_cb(_, cb: CallbackQuery):
    plugin = str(cb.data.split(":")[1])

    try:
        buttons = [
            InlineKeyboardButton(f"{i}", f"bot_help_cmd:{plugin}:{i}")
            for i in sorted(Config.BOT_HELP[plugin]["commands"])
        ]
    except KeyError:
        await cb.answer("No description for this plugin", show_alert=True)
        return

    buttons = [buttons[i : i+2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton("back", "help_data:bothelp")])

    caption = (
        f"Plugin: {plugin}\n"
        f"Plugin info: {Config.BOT_HELP[plugin]['info']}\n\n"
        f"Commands: {len(sorted(Config.BOT_HELP[plugin]['commands']))}"
    )

    try:
        await cb.edit_message_text(
            caption,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        pass


@ShemuraBot.bot.on_callback_query(filters.regex(r"bot_help_cmd"))
async def bot_help_cmd_cb(_, cb: CallbackQuery):
    plugin = str(cb.data.split(":")[1])
    command = str(cb.data.split(":")[2])
    cmd_dict = Config.BOT_HELP[plugin]["commands"][command]
    result = ""

    if cmd_dict["parameters"] is None:
        result += f"**Command:** {cmd_dict['command']}"
    else:
        result += f"**Command:** {cmd_dict['command']} {cmd_dict['parameters']}"

    if cmd_dict["description"]:
        result += (
            f"\n\n**Description:** {cmd_dict['description']}"
        )

    if cmd_dict["example"]:
        result += f"\n\n**Example:** {cmd_dict['example']}"

    if cmd_dict["note"]:
        result += f"\n\n**Note: **{cmd_dict['note']}"

    buttons = [
        [
            InlineKeyboardButton("back", f"bot_help_menu:{plugin}"),
            InlineKeyboardButton("close", "help_data:botclose"),
        ]
    ]

    try:
        await cb.edit_message_text(
            result,
            ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        pass



@ShemuraBot.bot.on_callback_query(filters.regex(r"help_data"))
async def help_cb(_, cb: CallbackQuery):
    action = str(cb.data.split(":")[1])

    if action == "close":
        await cb.edit_message_text(
            "Help Menu Close",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Reopen", "help_data:reopen")]]),
        )
    # elif action == "reopen":
    #     buttons, pages = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU))
    #     caption = (
    #         f"Plugin: {len(Config.CMD_INFO)} \n"
    #         f"Total commands: {len(Config.CMD_MENU)} \n"
    #         f"Page: {1} | {pages}"
    #     )
    #     await cb.edit_message_text(
    #         caption,
    #         reply_markup=InlineKeyboardMarkup(buttons),
    #     )
    elif action == "botclose":
        await cb.message.delete()
    elif action == "bothelp":
        buttons = await gen_bot_help_buttons()
        await cb.edit_message_text(
            HELP_MESSAGE,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif action == "source":
        buttons = [
            [
                InlineKeyboardButton("PM", url="https://t.me/afsfafasfawfas" ),
                InlineKeyboardButton("Back", "help_data:start"),
                InlineKeyboardButton("Close", "help_data:close"),
            ],
        ]

        await cb.edit_message_text(
            "Contact if you want",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif action == "start":
        buttons = start_button()
        await cb.edit_message_text(
            START_MSG.format(cb.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


